from django.contrib import admin
from .models import PhoneOtp, EmailOpt, User, FollowUps
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "name",
        "mobile",
        "date_joined",
        "last_login",
        "is_admin",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "username", "mobile")
    readonly_fields = ("id", "date_joined", "last_login")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(User, AccountAdmin)
admin.site.register(PhoneOtp)
admin.site.register(EmailOpt)
admin.site.register(FollowUps)
