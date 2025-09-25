from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Task, Group

class TaskForm(forms.ModelForm):
    title = forms.CharField(label='Name')

    PRIORITIES_CHOICE=[
        (1, 'Urgent'),
        (2, 'High'),
        (3, 'Neutral'),
        (4, 'Low')        
    ]

    priority = forms.ChoiceField(choices=PRIORITIES_CHOICE)

    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'priority']   

class AddToGroupForm(forms.ModelForm):    

    class Meta:
        model = Task
        fields = ['group']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddToGroupForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=self.request.user)
        self.fields['group'].empty_label = '- no group selected -'
        self.fields['group'].required = False
        self.fields['group'].widget.attrs.update({
            'class': 'mt-1 block w-full rounded-md bg-gray-100 border border-gray-300 px-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-600'
        })