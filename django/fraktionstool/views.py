from django.views.generic import ListView
from fraktionstool.forms import GremiumSelectionForm
from fraktionstool.models import Gremium, Vorhaben
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

class VorhabenList(ListView):
    """ Displays a list of Vorhaben objects and allows a user to specify
    a Gremium object to display only Vorhaben objects linked to such a
    Gremium.
    """
    paginate_by = 10
    template_name = 'vorhaben.html'
    context_object_name = 'vorhaben'

    def get_context_data(self, **kwargs):
        context = super(VorhabenList, self).get_context_data(**kwargs)
        context['form'] = GremiumSelectionForm()
        context['gremium'] = self.gremium

        return context

    def get_queryset(self):
        """ Returns a queryset for Vorhaben objects. If a 'gremium' parameter
        has been passed, only those Vorhaben objects are returned, that are
        linked to the Gremium object specified. Otherwise all Vorhaben objects
        are returned.
        """
        self.gremium = None
        if 'gremium' in self.kwargs:
            gremium_id = self.kwargs['gremium']
            return Vorhaben.objects.filter(gremien__in=gremium_id)
        else:
            return Vorhaben.objects.all()

    def post(self, request, *args, **kwargs):
        """ Reacts to the POST request of the GremiumSelectionForm. If a valid
        Gremium object has been selected, this list view is reloaded to display
        the linked Vorhaben objects. Otherwise, the redirect is made without a
        Gremium object.
        """
        form = GremiumSelectionForm(request.POST or None)
        if form.is_valid():
            gremium_id = form.cleaned_data['gremium'].id
            return HttpResponseRedirect(reverse('ftool-home-gremium',
                 kwargs={'gremium': gremium_id}))
        else:
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
