from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # اظهار الحقول الأساسية والساعات في الجدول
    list_display = ('id', 'student', 'status', 'volunteer_hours', 'applied_at')
    
    # إضافة فلتر للحالة والتاريخ بالجنب
    list_filter = ('status', 'applied_at')
    
    # البحث باسم المستخدم
    search_fields = ('student__username',)
    
    # ميزة التعديل السريع للحالة والساعات من الجدول
    list_editable = ('status', 'volunteer_hours')