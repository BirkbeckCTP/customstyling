import os

from django import forms

from plugins.customstyling import plugin_settings


class StylingForm(forms.Form):
    css = forms.CharField(
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        self.journal = kwargs.pop('journal')
        super(StylingForm, self).__init__(*args, **kwargs)
        open_path = os.path.join(
            plugin_settings.BASE_CSS_PATH,
            str(self.journal.pk),
            'custom.css',
        )

        if os.path.isfile(open_path):
            with open(open_path) as css_file:
                css = css_file.read()
                self.fields['css'].initial = css
        else:
            self.fields['css'].initial = ''

    def save(self):
        css = self.cleaned_data['css']

        path = os.path.join(
            plugin_settings.BASE_CSS_PATH,
            str(self.journal.pk),
        )
        file = os.path.join(path, 'custom.css')
        if not os.path.exists(path):
            os.makedirs(path)

        with open(file, 'w') as css_file:
            css_file.write(css)
            css_file.close()
