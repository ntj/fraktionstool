from django.views.generic import ListView
from fraktionstool.forms import GremiumSelectionForm, MessageForm
from fraktionstool.forms import AbstimmungsForm
from fraktionstool.models import Gremium, Vorhaben, Nachricht
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

class NachrichtenList(ListView):
    """ Displays a list of Nachricht objects and allows a user to
    specify a Gremium and Vorhaben objects to display only Nachricht
    objects linked to those.
    """
    paginate_by = 10
    template_name = 'nachrichten.html'
    context_object_name = 'nachrichten'

    def get_context_data(self, **kwargs):
        context = super(NachrichtenList, self).get_context_data(**kwargs)
        # Provide initial form data
        initial_form_data = {}
        for field in ['gremium', 'vorhaben', 'show_all']:
            if field in self.kwargs:
                initial_form_data[field] = self.kwargs[field]
        if 'show_all' in initial_form_data:
            show_all_value = bool(int(initial_form_data['show_all']))
        else:
            show_all_value = False
        initial_form_data['show_all'] = show_all_value
        # Create extra context
        form = GremiumSelectionForm(initial=initial_form_data)

        # Narrow list of gremien to those the user is member of
        if not show_all_value:
            gremium_field = form.fields['gremium']
            gremium_field.queryset = gremium_field.queryset.filter(
                    member=self.request.user)

        vorhaben_field = form.fields['vorhaben']

        if 'gremium' in self.kwargs:
            vorhaben_field.queryset = vorhaben_field.queryset.filter(
                    gremien=self.kwargs['gremium'])
        else:
            first_gremium_id = form.fields['gremium'].queryset.order_by('name')[0].id
            vorhaben_field.queryset = vorhaben_field.queryset.filter(
                    gremien=first_gremium_id)

        if 'vorhaben' in self.kwargs:
            selected_vorhaben_id = self.kwargs['vorhaben']
        else:
            if(bool(vorhaben_field.queryset)):
                selected_vorhaben_id = vorhaben_field.queryset.order_by('name')[0].id
            else:
                selected_vorhaben_id = -1

        if int(selected_vorhaben_id) >= 0:
            selected_vorhaben = vorhaben_field.queryset.filter(
                id=selected_vorhaben_id).get()
            context['abstimmungsform'] = AbstimmungsForm(
                instance=selected_vorhaben)
            context['nachrichtform'] = MessageForm()

        context['form'] = form
        return context

    def get_queryset(self):
        """ Returns a queryset for Vorhaben objects. If a 'gremium' parameter
        has been passed, only those Vorhaben objects are returned, that are
        linked to the Gremium object specified. Otherwise all Vorhaben objects
        are returned.
        """
        if 'gremium' in self.kwargs and 'vorhaben' in self.kwargs:
            vorhaben_id = int(self.kwargs['vorhaben'])
            nachrichten = Nachricht.objects.filter(vorhaben_id=vorhaben_id)
        else:
            gremium_id = Gremium.objects.filter(member = self.request.user)[0].id
            v_qset = Vorhaben.objects.filter(gremien= gremium_id)
            if v_qset:
                vorhaben_id = v_qset[0]
                nachrichten =  Nachricht.objects.all().filter(
                    gremium=gremium_id,vorhaben=vorhaben_id)
            else:
                return Nachricht.objects.none()
        return nachrichten.order_by('-id');

    def post(self, request, *args, **kwargs):
        """ Reacts to the POST request of the GremiumSelectionForm. If a valid
        Gremium object has been selected, this list view is reloaded to display
        the linked Vorhaben objects. Otherwise, the redirect is made without a
        Gremium object.
        """
        if request.POST:
            if 'update_messages' in request.POST:
                form = GremiumSelectionForm(request.POST)
                if form.is_valid():
                    gremium = form.cleaned_data['gremium']
                    gremium_id = gremium.id
                    vorhaben = form.cleaned_data['vorhaben']
                    if vorhaben:
                        vorhaben_id = vorhaben.id
                    else:
                        vorhaben_id = 0

                    # test if only gremien the user is member of should be
                    # displayed
                    if not form.cleaned_data['show_all']:
                        show_all = 0
                        gremium_field = form.fields['gremium']

                        # Test if selected gremium is within gremien the user is
                        # member of
                        gremium_field.queryset = gremium_field.queryset.filter(
                                member=self.request.user)

                        if not gremium_field.queryset.filter(id = gremium.id).exists():
                            # Select first gremium which user is member of
                            gremium_id = gremium_field.queryset.order_by(
                                    'name')[0].id
                    else:
                        show_all = 1

                    # Update vorhaben to first of selected gremium
                    tmp_qset = form.fields['vorhaben'].queryset.filter(
                            gremien = gremium_id).order_by('name')
                    if bool(tmp_qset):
                        if not vorhaben in tmp_qset:
                            vorhaben = tmp_qset[0]
                    else:
                        vorhaben_id = -1

                    if vorhaben:
                        gremien_to_vorhaben = vorhaben.gremien.all()
                        if not gremium in gremien_to_vorhaben:
                            tmp_qset = gremium.vorhaben_set.all().exclude(
                                geschlossen=True).order_by('name')
                            if bool(tmp_qset):
                                vorhaben = tmp_qset[0]
                            else:
                                vorhaben_id = -1
                    else:
                        vorhaben_id = -1
                    if(vorhaben_id != -1):
                        vorhaben_id = vorhaben.id

                    return HttpResponseRedirect(reverse('ftool-home-gremium',
                         kwargs={'gremium': gremium_id, 'show_all': show_all,
                                     'vorhaben': vorhaben_id}))

            elif 'create_message' in request.POST:
                message_form = MessageForm(request.POST)
                gremium_form = GremiumSelectionForm(request.POST)
                if message_form.is_valid() and gremium_form.is_valid():
                    text = message_form.cleaned_data['text']
                    gremium_id = gremium_form.cleaned_data['gremium'].id
                    vorhaben_id = gremium_form.cleaned_data['vorhaben'].id
                    Nachricht.objects.create(text=text, gremium_id=gremium_id,
                            vorhaben_id=vorhaben_id, owner=request.user)
                    if gremium_form.cleaned_data['show_all']:
                        show_all = 1
                    else:
                        show_all = 0
                    return HttpResponseRedirect(reverse('ftool-home-gremium',
                         kwargs={'gremium': gremium_id, 'show_all': show_all,
                                     'vorhaben': vorhaben_id}))
            elif 'change_abstimmung' in request.POST:
                abstimmungs_form = AbstimmungsForm(request.POST)
                gremium_form = GremiumSelectionForm(request.POST)
                if abstimmungs_form.is_valid() and gremium_form.is_valid():
                    gremium_id = gremium_form.cleaned_data['gremium'].id
                    abstimmung = abstimmungs_form.cleaned_data['abstimmung']
                    vorhaben = gremium_form.cleaned_data['vorhaben']
                    
                    if gremium_form.cleaned_data['show_all']:
                        show_all = 1
                    else:
                        show_all = 0
                    vorhaben.abstimmung = abstimmung
                    vorhaben.save()
                    return HttpResponseRedirect(reverse('ftool-home-gremium',
                         kwargs={'gremium': gremium_id, 'show_all': show_all,
                                     'vorhaben': vorhaben.id}))

        return HttpResponseRedirect(reverse('ftool-home'))

def list_gremien(request):
    """ Return a JSON object with IDs and names of Gremium model objects.
    If the GET parameter 'onlyown' contains anything else than '0', only the
    Gremium objects are returned, of which the requesting user is part of.
    """
    only_user = bool(int(request.GET.get('onlyown', 0)))
    if only_user:
        gremien_qs = request.user.gremium_set.all()
    else:
        gremien_qs = Gremium.objects.all()

    gremien = {}
    for g in gremien_qs:
        gremien[g.id] = g.name

    return HttpResponse(json.dumps(gremien))

def list_vorhaben(request):
    """ Return a JSON object with IDs and names of Vorhaben model objects.
    If the gremium_id parameter is None, all Vorhaben objects are returned.
    """
    gremium_id = request.GET.get('gremium_id', None)
    if gremium_id:
        gremium_ids = [int(gremium_id)]
        vorhaben_qs = Vorhaben.objects.filter(gremien__in=gremium_ids)
    else:
        vorhaben_qs = Vorhaben.objects.all()

    vorhaben = {}
    for v in vorhaben_qs.exclude(geschlossen__exact=True):
        vorhaben[v.id] = v.name
    return HttpResponse(json.dumps(vorhaben))

def list_nachrichten(request):
    """ Return a JSON object with IDs and names of Nachricht model objects.
    If the gremium_id and the vorhaben_id parameter is None, all Nachrichten
    objects are returned.
    """
    gremium_id = request.GET.get('gremium_id', None)
    vorhaben_id = request.GET.get('vorhaben_id', None)
    if gremium_id and vorhaben_id:
        nachrichten_qs = Nachricht.objects.filter(gremium_id=gremium_id,
            vorhaben_id=vorhaben_id)
    elif gremium_id:
        nachrichten_qs = Nachricht.objects.filter(gremium_id=gremium_id)
    elif vorhaben_id:
        nachrichten_qs = Nachricht.objects.filter(vorhaben_id=vorhaben_id)
    else:
        nachrichten_qs = Nachricht.objects.all()

    nachrichten = {}
    for n in nachrichten_qs.oder_by('-id'):
        nachrichten[n.id] = n.text
    
    return HttpResponse(json.dumps(nachrichten))
