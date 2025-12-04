from django import forms


class CodeUploadForm(forms.Form):
    file = forms.FileField(label='Upload source code file')
    language_hint = forms.CharField(
        required=False,
        max_length=50,
        help_text='Optional language hint: python, java, c, cpp'
    )
