from django.contrib import admin
from .models import CustomAccount
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomAccount, UserAdmin)
