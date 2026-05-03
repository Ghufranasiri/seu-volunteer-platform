from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Certificate


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'university_id', 'bio')}),
    )


admin.site.register(Certificate)