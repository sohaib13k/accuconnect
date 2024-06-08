from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ["friends", "sent_requests", "pending_requests"]
    readonly_fields = ("sent_request_count", "sent_request_tmstmp")


admin.site.register(UserProfile, UserProfileAdmin)
