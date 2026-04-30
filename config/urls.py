"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

# دالة لتحويل المستخدم من الصفحة الرئيسية إلى قائمة الفرص مباشرة
def home_redirect(request):
    return redirect('opportunities:opportunity_list') 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # الصفحة الرئيسية (تم تعديلها لتعرض الفرص فورًا)
    path('', home_redirect, name='home'),
    
    # روابط الحسابات (تسجيل الدخول، الخروج، إلخ)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # روابط التطبيقات الأخرى
    path('dashboard/', include('dashboard.urls')),
    path('opportunities/', include('opportunities.urls')),
    path('users/', include('users.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('', include('accounts.urls')),
]
