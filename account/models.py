from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
gender = (
    ("M", "Male"),
    ("F", "Female"),
    ("X", "Not Specified"),
)


class CustomAccount(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    gender = models.CharField(max_length=1, choices=gender, default="X")

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.first_name
