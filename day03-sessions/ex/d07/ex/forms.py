from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match.")
        return cleaned_data


class TipForm(forms.ModelForm):
    class Meta:
        model = models.Tip
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 50})
        }
        labels = {
            'content': 'Tip'
        }
