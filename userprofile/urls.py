# accounts/urls.py
from django.urls import path
from userprofile.views import list_friend

urlpatterns = [
    path("find/", list_friend, name="register"),
    path("friend/", list_friend, name="list_friend"),
]
