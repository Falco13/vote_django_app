from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserRegisterForm, MyLoginForm, EditUserInfoForm
from accounts.tokens import account_activation_token
from accounts.models import User
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings


class SignUpView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            send_mail(subject=subject,
                      message=message,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[form.cleaned_data['email'], ])
            messages.success(request, 'Please Confirm your email to complete registration.')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):
    def get(self, request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend', *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account have been confirmed.')
            return redirect('poll_app:home')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('poll_app:home')


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = MyLoginForm


class MyLogoutView(LoginRequiredMixin, LogoutView):
    next_page = None


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


class EditUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/edit_user_info.html'
    form_class = EditUserInfoForm
    success_url = reverse_lazy('accounts:profile')
    success_message = 'User information changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/delete_user.html'
    success_url = reverse_lazy('poll_app:home')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Your password has been changed successfully'
