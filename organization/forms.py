from django import forms

from .models import organization, Member, work
from django.forms import Form, ModelForm, DateField, widgets

class create_organization_form(forms.ModelForm):
    
    class Meta:
        model = organization
        fields = ('name', 'description', 'cover')

class update_organization_form(forms.ModelForm):
    
    class Meta:
        model = organization
        fields = ('description', 'cover', 'owner', 'admins', 'members')

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org')
        super(update_organization_form, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = org.members
        self.fields['admins'].queryset = org.members
        self.fields['members'].queryset = org.members
        

class add_member(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('user',)

    
class create_work_form(forms.ModelForm):
    
    class Meta:
        model = work
        fields = ('title', 'description', 'assigned_to', 'due_date')
    
        widgets = {
            'due_date': widgets.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org')
        super(create_work_form, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = org.members

class update_work_form(forms.ModelForm):
    
    class Meta:
        model = work
        fields = ('files', 'is_complete')
    