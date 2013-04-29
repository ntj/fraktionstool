from django.views.generic.edit import FormView
from fraktionstool.forms import GremiumSelectionForm

class VorhabenView(FormView):
	template_name = 'vorhaben.html'
	form_class = GremiumSelectionForm
