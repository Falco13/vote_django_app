from django import forms
from django.core.exceptions import ValidationError

from poll_app.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {'comment_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), }

    def clean_comment_text(self):
        comment_text = self.cleaned_data['comment_text']
        if len(comment_text) > 500:
            raise ValidationError('No more than 500 characters please')
        return comment_text
