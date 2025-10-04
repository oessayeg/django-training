from django import forms


class TextForm(forms.Form):
    text_field = forms.CharField(label="Text", max_length=100)
