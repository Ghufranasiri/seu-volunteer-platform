from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Certificate


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('phone', 'university_id', 'bio', 'role', 'major', 'interests')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('phone', 'university_id', 'bio', 'role', 'major', 'interests')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Certificate)