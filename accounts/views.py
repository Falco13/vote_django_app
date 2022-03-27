from django.shortcuts import render
from django.contrib.auth.views import LoginView
from accounts.forms import MyLoginForm


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = MyLoginForm
