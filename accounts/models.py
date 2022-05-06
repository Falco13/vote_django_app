from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
