from django.shortcuts import render
from opportunities.models import Opportunity


def dashboard_view(request):
    opportunities = Opportunity.objects.all()

    context = {
        "opportunities": opportunities,
        "total_opportunities": opportunities.count(),
        "total_applications": 0,
        "pending_applications": 0,
        "applications": [],
    }

    return render(request, "dashboard/dashboard.html", context)
