from django.urls import path
from poll_app.views import HomeView, detail_question, ResultsView, AboutView, vote

app_name = 'poll_app'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug:slug>/', detail_question, name='detail'),
    path('results/<slug:slug>/', ResultsView.as_view(), name='results'),
    path('vote/<slug:slug>', vote, name='vote'),
    path('about/', AboutView.as_view(), name='about'),
]
