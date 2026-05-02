from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<int:pk>/", views.apply_opportunity, name="apply_opportunity"),
]