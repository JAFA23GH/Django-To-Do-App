from django.shortcuts import render

from django import forms

from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login

# from myapp.forms import MyForm


# Create your views here.

class SignUpView(FormView):    
    template_name = 'authentication/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    

class MyLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

