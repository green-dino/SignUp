from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        #list all fields
        fields = [ ]
