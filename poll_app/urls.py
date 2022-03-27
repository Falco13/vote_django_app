from django.urls import path
from poll_app.views import HomeView, DetailView, ResultsView, vote

app_name = 'poll_app'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/<int:pk>/', DetailView.as_view(), name='detail'),
    path('results/<int:pk>/', ResultsView.as_view(), name='results'),
    path('vote/<int:pk>', vote, name='vote'),
]
