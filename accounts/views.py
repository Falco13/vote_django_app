from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from accounts.forms import UserRegisterForm, MyLoginForm
from django.views.generic.edit import CreateView


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = MyLoginForm


class MyLogoutView(LogoutView):
    next_page = None
