from django.views.generic.edit import FormView
from fraktionstool.forms import GremiumSelectionForm
from fraktionstool.models import Gremium, Vorhaben
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

class VorhabenView(FormView):
    template_name = 'vorhaben.html'
    form_class = GremiumSelectionForm

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('home'))

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
