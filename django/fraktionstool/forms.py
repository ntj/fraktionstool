from django import forms
from fraktionstool.models import Gremium, Vorhaben, Nachricht

class GremiumSelectionForm(forms.Form):
	gremium = forms.ModelChoiceField(empty_label=None,
		queryset=Gremium.objects.all())
	vorhaben = forms.ModelChoiceField(empty_label=None,
		queryset=Vorhaben.objects.all())
	my_gremien = forms.BooleanField(
		label='Nur meine Gremien',
		required=False)

class MessageForm(forms.ModelForm):
	class Meta:
		model = Nachricht
		fields = ["text"]
