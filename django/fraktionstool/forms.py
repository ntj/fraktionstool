from django import forms
from fraktionstool.models import Gremium

class GremiumSelectionForm(forms.Form):
	gremium = forms.ModelChoiceField(
		queryset=Gremium.objects.all())
	my_gremien = forms.BooleanField(
		label='Nur meine Gremien')
