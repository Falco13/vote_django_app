from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponseForbidden
from poll_app.models import Question, Vote


def can_change_vote(view_func):
    def _wrapped_view(request, *args, **kwargs):
        question = get_object_or_404(Question, slug=kwargs['slug'])
        user_vote = Vote.objects.filter(voter=request.user, question=question).first()

        if user_vote:
            # Если голос был отдан менее 30 дней назад
            time_difference = timezone.now() - user_vote.created_at
            if time_difference < timedelta(days=30):
                # Запрещаем изменение голоса
                return HttpResponseForbidden("You cannot change your vote within 30 days.")

        # Если условия не нарушены, выполняем оригинальную функцию
        return view_func(request, *args, **kwargs)

    return _wrapped_view
