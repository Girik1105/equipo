from django import forms 
from . import models 
from django.forms import Form, ModelForm, DateField, widgets


class doodle_form(forms.ModelForm):

    class Meta:
        model = models.doodle
        fields = ('title', 'body') 
        labels = {
            "body":'',
        }


class todo_form(forms.ModelForm):

    class Meta:
        model = models.to_do
        fields = ('title', 'description', 'due_date') 
        labels = {
            "description":'',
            "due_date":"Due Date ",
        }
        widgets = {
            'due_date': widgets.DateInput(attrs={'type': 'date'})
        }