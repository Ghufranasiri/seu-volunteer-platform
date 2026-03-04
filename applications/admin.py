from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'opportunity', 'status', 'applied_at') # الأعمدة التي ستظهر للمشرف
    list_filter = ('status', 'applied_at') # فلاتر جانبية للبحث
    search_fields = ('student__username', 'opportunity__title') # إمكانية البحث باسم الطالب أو الفرصة
    list_editable = ('status',) # تمكين المشرف من تغيير الحالة مباشرة من القائمة
    