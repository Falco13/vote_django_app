from django.urls import path
from poll_app.views import HomeView, DetailView, ResultsView, AboutView, vote

app_name = 'poll_app'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug:slug>/', DetailView.as_view(), name='detail'),
    path('results/<slug:slug>/', ResultsView.as_view(), name='results'),
    path('vote/<slug:slug>', vote, name='vote'),
    path('about/', AboutView.as_view(), name='about'),
]
