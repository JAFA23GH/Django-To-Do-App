from django.urls import path
from .views import (TaskList, TaskCreation, TaskDelete, TaskEdit, 
                    AddTaskToGroup)

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskList.as_view(), name='home'),    
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('task-create/', TaskCreation.as_view(), name='creation'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
    path('task-update/<int:pk>', TaskEdit.as_view(), name='task-edit'),
    path('move-task/<int:pk>', AddTaskToGroup.as_view(), name='add-task-group')    
]
