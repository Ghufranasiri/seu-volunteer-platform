from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
]