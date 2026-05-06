from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),

    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),

    path('create/', views.create_opportunity, name='create_opportunity'),

    path('<int:pk>/edit/', views.edit_opportunity, name='edit_opportunity'),

    path('<int:pk>/delete/', views.delete_opportunity, name='delete_opportunity'),

    path(
        '<int:pk>/approve/',
        views.approve_opportunity,
        name='approve_opportunity'
    ),

    path(
        '<int:pk>/reject/',
        views.reject_opportunity,
        name='reject_opportunity'
    ),
]