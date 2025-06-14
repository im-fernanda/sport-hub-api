from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    is_first_login = models.BooleanField(default=True)
