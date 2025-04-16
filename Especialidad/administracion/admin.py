from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Usuario


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": (
            "first_name",
            "last_name", 
            "email", 
            "password", 
            "date_of_birth")}
        ),
        ("Permissions", {"fields": (
            "is_staff", 
            "is_active", 
            "groups", 
            "user_permissions")}
        ),
    )
    add_fieldsets = (
        ( None, {"fields": (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Usuario, CustomUserAdmin)
