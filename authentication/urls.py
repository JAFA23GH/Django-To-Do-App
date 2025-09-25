from django.urls import path

from .views import MyLoginView, SignUpView

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='sign_up')
]
