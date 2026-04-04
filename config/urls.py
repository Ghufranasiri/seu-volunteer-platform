"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path
from django.http import HttpResponse

def home(request):
    return HttpResponse("SEU Volunteer Platform is running ✅")

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Public Pages
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Opportunities
    path('opportunities/', views.opportunities_list, name='opportunities_list'),
    path('opportunities/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    
    # Student Dashboard
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('hours/', views.hours_tracking, name='hours_tracking'),
    path('certificates/', views.certificates_view, name='certificates'),
    
    # Agency Dashboard
    path('dashboard/agency/', views.agency_dashboard, name='agency_dashboard'),
    
    # Admin Dashboard
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('', home),
    path('dashboard/', include('dashboard.urls')),
    path('opportunities/', include('opportunities.urls')),
]
