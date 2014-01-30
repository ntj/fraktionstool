from django import forms
from fraktionstool.widgets import OptionClassesSelect
from fraktionstool.models import Gremium, Vorhaben, Nachricht

def highlight_messages(option_value):
    has_messages = Nachricht.objects.filter(vorhaben=option_value).exists()
    return 'has_messages' if has_messages else 'has_no_messages'

class VorhabenModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nummer + " - " + obj.name

class GremiumSelectionForm(forms.Form):
    gremium = forms.ModelChoiceField(empty_label=None,
        queryset=Gremium.objects.all(), required=False)

    vorhaben = VorhabenModelChoiceField(required=False, empty_label=None,
        widget=OptionClassesSelect(
            get_option_class=highlight_messages,selected_index=0),
        queryset=Vorhaben.objects.exclude(geschlossen=True))

    show_all = forms.BooleanField(
            label='Alle Gremien anzeigen',
            required=False)

    def mysize(self,nrSize):
        resSize = min(nrSize, 30)
        self.fields['vorhaben'].widget.attrs['size'] = str(resSize)

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
