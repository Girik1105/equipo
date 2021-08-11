from django import forms 
from django.forms import Form, ModelForm, DateField, widgets

from . import models 


class profile_form(forms.ModelForm):
    class Meta:
        model = models.user_profile
        fields = ('name','profile_picture', 'background', 'gender', 'birth_date', 'location')

        widgets = {
            'birth_date': widgets.DateInput(attrs={'type': 'date'})
        }