from datetime import timedelta

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from poll_app.models import Question, Vote


def can_change_vote(view_func):
    def _wrapped_view(request, *args, **kwargs):
        slug = kwargs.get('slug')
        question = get_object_or_404(Question, slug=kwargs['slug'])
        user_vote = Vote.objects.filter(voter=request.user, question=question).first()

        if user_vote:
            time_difference = timezone.now() - user_vote.created_at
            if time_difference < timedelta(days=30):
                messages.error(request, "You cannot change your vote within 30 days.")
                return HttpResponseRedirect(reverse('poll_app:results', args=(slug,)))
        return view_func(request, *args, **kwargs)

    return _wrapped_view
