# -*- coding: utf8 -*-

from django.forms.widgets import Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from itertools import chain

class OptionClassesSelect(Select):

    def __init__(self, attrs=None, choices=(), get_option_class=None,
                selected_index=None):
        super(OptionClassesSelect, self).__init__(attrs, choices)
        self.get_option_class = get_option_class
        self.selected_index = selected_index

    def render_option(self, selected_choices, option_value, option_label, i):
        if self.get_option_class:
            cls = self.get_option_class(option_value)
            cls_html = 'class=%s' % cls
        else:
            cls_html = '' 
        option_value = force_text(option_value)
        if self.selected_index == i:
            selected_html = mark_safe(' selected="selected"')
        elif option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html(u'<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           cls_html,
                           force_text(option_label))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for i, (option_value, option_label) in enumerate(
                chain(self.choices,choices)):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{0}">',
                        force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices,
                        *option, i=i))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices,
                         option_value, option_label, i))
        return '\n'.join(output)
