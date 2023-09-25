from django.db import models
from accounts.models import User


class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Question(models.Model):
    question_text = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    views = models.ManyToManyField(IpModel, related_name='post_views', blank=True)

    def __str__(self):
        return self.question_text

    def total_views(self):
        return self.views.count()

    class Meta:
        ordering = ['-created_at']

    @property
    def total_votes(self):
        return Vote.objects.filter(question=self.pk).count()


class Choice(models.Model):
    choice_text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

    @property
    def get_vote_count(self):
        return Vote.objects.filter(choice=self.pk).count()

    @property
    def percentage_vote(self):
        total_votes = Vote.objects.filter(question=self.question).count()
        vote_count = Vote.objects.filter(choice=self).count()
        if total_votes == 0:
            vote_in_percentage = 0
        else:
            vote_in_percentage = (vote_count / total_votes) * 100
        return vote_in_percentage


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    question_relation = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment_text

    class Meta:
        ordering = ['-created_at']
