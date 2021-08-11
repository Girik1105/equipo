from django import forms

from .models import organization, Member

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