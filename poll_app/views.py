from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from poll_app.models import Question, Choice, Vote


class HomeView(generic.ListView):
    template_name = 'poll_app/home.html'
    context_object_name = 'question_list'
    queryset = Question.objects.filter(is_active=True)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll_app/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll_app/results.html'


class AboutView(generic.TemplateView):
    template_name = 'poll_app/about.html'


def vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    if Vote.objects.filter(voter=request.user, question=question).exists():
        messages.error(request, "Already Voted on this choice")
        return HttpResponseRedirect(reverse('poll_app:results', args=(pk,)))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        Vote.objects.create(voter=request.user, choice=selected_choice, question=question)
        messages.success(request, "Thanks for your vote!")
        return HttpResponseRedirect(reverse('poll_app:results', args=(pk,)))
