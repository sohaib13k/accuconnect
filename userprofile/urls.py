# accounts/urls.py
from django.urls import path
from userprofile.views import list_friend, find_friend

urlpatterns = [
    path("find/", find_friend, name="find_friend"),
    path("friend/", list_friend, name="list_friend"),
]
