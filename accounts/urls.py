from django.urls import path
from accounts.views import MyLoginView

app_name = 'accounts'
urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
]
