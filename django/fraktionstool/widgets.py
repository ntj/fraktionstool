from django.forms.widgets import Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class OptionClassesSelect(Select):

    def __init__(self, attrs=None, choices=(), get_option_class=None):
        super(OptionClassesSelect, self).__init__(attrs, choices)
        self.get_option_class = get_option_class;

    def render_option(self, selected_choices, option_value, option_label):
        if self.get_option_class:
            cls = self.get_option_class(option_value)
            cls_html = 'class=%s' % cls
        else:
            cls_html = '' 
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           cls_html,
                           force_text(option_label))
