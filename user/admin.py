from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from user.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = 'status', 'email', 'is_superuser',
    fieldsets = (
        # (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'phone_number', 'role', 'status', 'tg_id')}),

        (_('Important dates'), {'fields': ('last_login',)}),
    )
