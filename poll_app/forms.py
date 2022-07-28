from django import forms
from poll_app.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {'comment_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), }
