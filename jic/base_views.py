from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

from .models import Task, Group
from .forms import TaskForm, AddToGroupForm

# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.filter(user=self.request.user)
        context['tasks'] = Task.objects.filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['groups'] = context['groups'].filter(name__startswith = search_input)
            context['tasks'] = context['tasks'].filter(title__startswith = search_input)
        
        context['search_input'] = search_input      
        return context   
        
   
class TaskCreation(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/task_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreation, self).form_valid(form)
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_confirm_delete.html'
    success_url = reverse_lazy('home')

class TaskEdit(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm    
    template_name = 'base/task_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_pk =  self.kwargs['pk']        
        context['tasks'] = Task.objects.filter(user=self.request.user)
        context['task_edit'] = Task.objects.filter(user=self.request.user, id = task_pk)
        return context  

class AddTaskToGroup(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = AddToGroupForm    
    template_name = 'base/add_task_to_group.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(AddTaskToGroup, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

 


    

    


