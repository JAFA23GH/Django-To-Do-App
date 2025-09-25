from django import forms
from base.models import Task, Group

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name']

class RemoveForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['group']

    def __init__(self, *args, **kwargs):
        super(RemoveForm, self).__init__(*args, **kwargs)
        self.group = None
        if 'group' in self.fields:
            self.fields['group'].empty_label = '- no group selected -'
            self.fields['group'].required = False
