from django.contrib import admin
 maryam-merge-fix
from django.urls import path, include
from dashboard import views as dashboard_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_panel/', admin.site.urls),

    path('', dashboard_views.home, name='home'),
    path('login/', dashboard_views.login_view, name='login'),
    path('logout/', dashboard_views.logout_view, name='logout'),
    path('signup/', dashboard_views.register_view, name='signup'),
    path('profile/', include('student_profile.urls')),


from django.urls import include, path
from config import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

path('login/', views.login_view, name='login'),
path('register/', views.register_view, name='register'),
path('logout/', views.logout_view, name='logout'),

    path('dashboard/', include('dashboard.urls')),

    path('opportunities/', include('opportunities.urls')),

    path('applications/', include('applications.urls')),
    path('chatbot/', include('chatbot.urls')),

    path('users/', include('users.urls')),
    path('', include('accounts.urls')),
maryam-merge-fix
    path('i18n/', include('django.conf.urls.i18n')),

 

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)