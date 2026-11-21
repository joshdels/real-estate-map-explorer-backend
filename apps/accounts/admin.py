from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class OpenLotUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "role", "provider_id", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Open Lot Plans", {"fields": ("role", "provider_id")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2", "role", "provider_id")}),
    )
    search_fields = ("email",)
