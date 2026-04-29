from django.contrib import admin
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

    path('opportunities/', include('opportunities.urls')),
    path('users/', include('users.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('', include('accounts.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)