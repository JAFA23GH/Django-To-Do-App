from django.contrib import admin
from .models import Group, Task

# Register your models here.

class TaskAdmin (admin.ModelAdmin):
    readonly_fields = ['created_at']

admin.site.register(Group)
admin.site.register(Task, TaskAdmin)