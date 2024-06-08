from django.contrib import admin
from .models import CustomAccount, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

    extra = 0
    readonly_fields = ("friends", "sent_requests", "sent_request_count", "sent_request_tmstmp")


class CustomAccountAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.register(CustomAccount, CustomAccountAdmin)
