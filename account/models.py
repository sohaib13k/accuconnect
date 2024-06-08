from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

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


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomAccount, on_delete=models.CASCADE, related_name="profile"
    )
    friends = models.ManyToManyField("self")
    sent_requests = models.ManyToManyField("self")
    pending_requests = models.ManyToManyField("self")
    sent_request_count = models.IntegerField(default=0)
    sent_request_tmstmp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}'s Profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="570db2c4-59ea-4533-b65f-e2c02fec1454")
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
