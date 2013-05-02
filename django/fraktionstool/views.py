from django.views.generic.edit import FormView
from fraktionstool.forms import GremiumSelectionForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class VorhabenView(FormView):
    template_name = 'vorhaben.html'
    form_class = GremiumSelectionForm

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('home'))
