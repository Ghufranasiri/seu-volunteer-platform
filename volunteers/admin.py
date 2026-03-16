from django.contrib import admin
from .models import (
    Organization, Category, Opportunity, VolunteerRegistration,
    VolunteerHours, Certificate, Review, Impact, Announcement
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'is_verified', 'is_active', 'created_at')
    list_filter = ('is_verified', 'is_active', 'city')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'icon')
    search_fields = ('name',)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'category', 'status', 'start_date', 'max_volunteers', 'registered_count')
    list_filter = ('status', 'difficulty', 'category', 'is_featured', 'start_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('title', 'description', 'organization', 'category', 'image')
        }),
        ('التفاصيل', {
            'fields': ('required_hours', 'difficulty', 'max_volunteers')
        }),
        ('الموقع والوقت', {
            'fields': ('address', 'city', 'start_date', 'end_date')
        }),
        ('المتطلبات', {
            'fields': ('requirements', 'skills')
        }),
        ('الحالة', {
            'fields': ('status', 'is_featured')
        }),
        ('البيانات الإدارية', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VolunteerRegistration)
class VolunteerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'opportunity', 'status', 'registered_at')
    list_filter = ('status', 'registered_at')
    search_fields = ('volunteer__username', 'opportunity__title')
    readonly_fields = ('registered_at', 'approved_at')


@admin.register(VolunteerHours)
class VolunteerHoursAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'opportunity', 'hours', 'date_completed', 'status')
    list_filter = ('status', 'date_completed')
    search_fields = ('volunteer__username', 'opportunity__title')
    readonly_fields = ('submitted_at', 'updated_at')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'volunteer', 'level', 'issued_date', 'is_verified')
    list_filter = ('level', 'is_verified', 'issued_date')
    search_fields = ('title', 'volunteer__username')
    readonly_fields = ('issued_date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'opportunity', 'rating', 'created_at', 'is_verified')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('volunteer__username', 'opportunity__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Impact)
class ImpactAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'total_hours', 'total_opportunities', 'total_certificates', 'impact_points')
    list_filter = ('updated_at',)
    search_fields = ('volunteer__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
