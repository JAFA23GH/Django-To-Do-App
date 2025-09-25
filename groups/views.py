from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from base.models import Task, Group

from .forms import GroupForm, RemoveForm
from base.forms import TaskForm

# Create your views here.

class TaskGroupList(LoginRequiredMixin, ListView, FormMixin):
    model = Task
    context_object_name = 'group_tasks'
    template_name = 'groups/task_group_list.html'
    form_class = RemoveForm 

    def get_context_data(self, **kwargs):
        context = super(TaskGroupList, self).get_context_data(**kwargs)
        group_pk = self.kwargs['pk']
        context['group'] = Group.objects.get(id = group_pk)
        context['group_tasks'] = (
            Task.objects.filter(user=self.request.user, group=group_pk)
            .order_by('priority', '-created_at')
        )

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['group_tasks'] = context['group_tasks'].filter(title__startswith = search_input)

        context['search_input'] = search_input
        return context     
    
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id = task_id)
        task.group = None
        task.save()
        group_pk = self.kwargs['pk']
        return redirect('group', pk = group_pk)

class GroupCreation(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GroupCreation, self).form_valid(form)  
    
class GroupEdit(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm    
    template_name = 'groups/group_form.html'
    success_url = reverse_lazy('group')

    def get_success_url(self):
        return reverse_lazy('group', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        return context

class GroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    context_object_name = 'group'
    template_name = 'groups/group_confirm_delete.html'
    success_url = reverse_lazy('home')    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.get_object()
        return context
    
class GroupTaskCreation(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/task_form.html'
    success_url = reverse_lazy('group')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        group_id = self.kwargs['pk']
        group_instance = Group.objects.get(id = group_id)
        form.instance.group = group_instance
        form.instance.save()
        return super(GroupTaskCreation, self).form_valid(form)       
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('group', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['group'] = Group.objects.get(id=self.kwargs['pk'])
        except Group.DoesNotExist:
            pass
        return context
 
class GroupTaskEdit(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/task_form.html'

    def get_success_url(self):
        group = self.kwargs['pk1']
        return reverse_lazy('group', kwargs={'pk': group})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['group'] = Group.objects.get(id=self.kwargs['pk1'])
        except Group.DoesNotExist:
            pass
        return context
    
class GroupTaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_confirm_delete.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(GroupTaskDelete, self).get_context_data(**kwargs)
        group_id = self.kwargs['pk1']
        context['group'] = Group.objects.get(id = group_id)
        return context