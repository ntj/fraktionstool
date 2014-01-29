from django import forms
from fraktionstool.widgets import OptionClassesSelect
from fraktionstool.models import Gremium, Vorhaben, Nachricht

def highlight_messages(option_value):
    has_messages = Nachricht.objects.filter(vorhaben=option_value).exists()
    return 'has_messages' if has_messages else 'has_no_messages'

class GremiumSelectionForm(forms.Form):
    gremium = forms.ModelChoiceField(empty_label=None,
        queryset=Gremium.objects.all().order_by('name'), required=False)

    vorhaben = forms.ModelChoiceField(required=False, empty_label=None,
        widget=OptionClassesSelect(
            get_option_class=highlight_messages,selected_index=0),
        queryset=Vorhaben.objects.exclude(geschlossen=True).order_by('name'))

    show_all = forms.BooleanField(
            label='Alle Gremien anzeigen',
            required=False)

    def mysize(self,nrSize):
        print(nrSize)
        self.fields['vorhaben'].widget.attrs['size'] = str(nrSize)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Nachricht
        fields = ["text"]
        widgets = {
          'text': forms.Textarea(attrs={'rows':'6'}),
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Diskussion"
