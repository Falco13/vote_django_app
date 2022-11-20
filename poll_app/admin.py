from django.contrib import admin
from poll_app.models import Question, Choice, Vote, Comment, IpModel


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text', 'slug']}),
                 ('Date information', {'fields': ['created_at']}),
                 ('Active', {'fields': ['is_active']})]
    inlines = [ChoiceInline]
    readonly_fields = ['created_at']
    list_display = ['id', 'question_text', 'slug', 'created_at', 'is_active']
    prepopulated_fields = {'slug': ('question_text',)}


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice', 'voter', 'created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'question_relation', 'comment_text', 'created_at', 'is_active']


@admin.register(IpModel)
class IpAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip']
