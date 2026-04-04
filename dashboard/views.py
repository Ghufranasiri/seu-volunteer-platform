from django.shortcuts import render

def dashboard_view(request):
    context = {
        "total_opportunities": 10,
        "total_applications": 25,
        "total_hours": 120
    }

    return render(request, "dashboard/dashboard.html", context)
from django.shortcuts import render

def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")
