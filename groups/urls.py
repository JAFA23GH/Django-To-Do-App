from django.urls import path
from .views import (TaskGroupList, GroupCreation, GroupEdit, 
                    GroupDelete, GroupTaskCreation, GroupTaskEdit,
                    GroupTaskDelete)

urlpatterns = [
    path('<int:pk>', TaskGroupList.as_view(), name='group'),
    path('create/', GroupCreation.as_view(), name='group-create'),    
    path('delete/<int:pk>', GroupDelete.as_view(), name='group-delete'),
    path('edit/<int:pk>', GroupEdit.as_view(), name='group-edit'),
    path('<int:pk>/task-create', GroupTaskCreation.as_view(), name='group-task-creation'),
    path('<int:pk1>/task-update/<int:pk>/', GroupTaskEdit.as_view(), name='group-task-edit'),
    path('<int:pk1>/task-delete/<int:pk>/', GroupTaskDelete.as_view(), name='group-task-delete')  
]
