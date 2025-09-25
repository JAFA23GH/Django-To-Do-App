from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name        

class Task(models.Model):

    PRIORITIES=[
        (1, 'Urgent'),
        (2, 'High'),
        (3, 'Neutral'),
        (4, 'Low'),
        (5, 'Complete')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.IntegerField(default=3, choices=PRIORITIES)
    created_at = models.DateTimeField(auto_now_add=True)     

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['priority']    

    def save(self, *args, **kwargs):
        if self.complete:
            self.priority = 5
        return super().save(*args, **kwargs)    

    def __str__(self):
        return self.title    
    
