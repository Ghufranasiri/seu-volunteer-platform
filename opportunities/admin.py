from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'location', 'date', 'hours', 'is_active')
    list_filter = ('is_active', 'category', 'date')
    search_fields = ('name', 'description', 'organization', 'location')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
