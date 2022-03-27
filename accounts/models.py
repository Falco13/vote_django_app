from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_activated = models.BooleanField(default=True)
