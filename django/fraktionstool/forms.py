from django import forms
from fraktionstool.models import Gremium, Vorhaben

class GremiumSelectionForm(forms.Form):
	gremium = forms.ModelChoiceField(
		queryset=Gremium.objects.all())
	vorhaben = forms.ModelChoiceField(
		queryset=Vorhaben.objects.all())
	my_gremien = forms.BooleanField(
		label='Nur meine Gremien',
		required=False)
