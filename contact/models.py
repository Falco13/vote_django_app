from django.db import models
from accounts.models import User


class Contact(models.Model):
    name_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=15)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f' Name: {self.email}, Text: {self.text}'

    class Meta:
        ordering = ['-created_at']
