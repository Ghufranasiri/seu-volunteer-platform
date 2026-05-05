from django.urls import path
from . import views

app_name = "opportunities"

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
 maryam-merge-fix

    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),

    path('create/', views.create_opportunity, name='create_opportunity'),
    path('edit/<int:pk>/', views.edit_opportunity, name='edit_opportunity'),
    path('delete/<int:pk>/', views.delete_opportunity, name='delete_opportunity'),

]