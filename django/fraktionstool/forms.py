from django import forms
from fraktionstool.widgets import OptionClassesSelect
from fraktionstool.models import Gremium, Vorhaben, Nachricht

def highlight_messages(option_value):
    has_messages = Nachricht.objects.filter(vorhaben=option_value).exists()
    return 'has_messages' if has_messages else 'has_no_messages'

class GremiumSelectionForm(forms.Form):
	gremium = forms.ModelChoiceField(empty_label=None,
		queryset=Gremium.objects.all())
	vorhaben = forms.ModelChoiceField(empty_label=None,
        widget=OptionClassesSelect(attrs={'size':'5'},
            get_option_class=highlight_messages,selected_index=0),
		queryset=Vorhaben.objects.exclude(geschlossen=True))
	my_gremien = forms.BooleanField(
		label='Nur meine Gremien',
		required=False)

class MessageForm(forms.ModelForm):
	class Meta:
		model = Nachricht
		fields = ["text"]
