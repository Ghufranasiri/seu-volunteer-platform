from django.urls import path
from . import views

urlpatterns = [
    # تأكدي أن اسم الدالة هنا يطابق ما هو موجود في views.py
    path('', views.dashboard, name='dashboard'),
]