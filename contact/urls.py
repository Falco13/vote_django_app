from django.urls import path
from contact.views import contact_view

app_name = 'contact'
urlpatterns = [
    path('contact/', contact_view, name='contact'),
]
