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
        # groups ordered alphabetically 
        base_groups_qs = Group.objects.filter(user=self.request.user)
        context['groups'] = base_groups_qs.order_by('name')
        # independent flag to know if user has any groups 
        context['has_any_groups'] = base_groups_qs.exists()
        # tasks without group, ordered by priority, then newest
        context['tasks_without_group'] = (
            Task.objects.filter(user=self.request.user, group__isnull=True)
            .order_by('priority', '-created_at')
        )
        # keep all tasks available if other parts need them with same ordering
        context['tasks'] = (
            Task.objects.filter(user=self.request.user)
            .order_by('priority', '-created_at')
        )

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['groups'] = context['groups'].filter(name__startswith = search_input)
            # apply search to both the full tasks list and tasks_without_group
            context['tasks'] = context['tasks'].filter(title__startswith = search_input)
            context['tasks_without_group'] = context['tasks_without_group'].filter(title__startswith = search_input)

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

    def get_success_url(self):
        # If created with a group context (e.g., from group create page), go back there
        group_id = self.request.GET.get('group')
        if group_id:
            try:
                return reverse_lazy('group', kwargs={'pk': int(group_id)})
            except Exception:
                pass
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.request.GET.get('group')
        if group_id:
            try:
                context['group'] = Group.objects.get(id=int(group_id))
            except Exception:
                pass
        return context
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        if getattr(obj, 'group_id', None):
            context['group'] = obj.group
        return context

    def get_success_url(self):
        obj = self.object
        if getattr(obj, 'group_id', None):
            return reverse_lazy('group', kwargs={'pk': obj.group_id})
        return super().get_success_url()

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
        # If this task belongs to a group, expose it for template back/cancel links
        obj = self.get_object()
        if getattr(obj, 'group_id', None):
            context['group'] = obj.group
        return context  

    def get_success_url(self):
        obj = self.object
        if getattr(obj, 'group_id', None):
            return reverse_lazy('group', kwargs={'pk': obj.group_id})
        return super().get_success_url()

class AddTaskToGroup(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = AddToGroupForm    
    template_name = 'base/add_task_to_group.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(AddTaskToGroup, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        obj = self.object
        if getattr(obj, 'group_id', None):
            return reverse_lazy('group', kwargs={'pk': obj.group_id})
        return super().get_success_url()

 


    

    


