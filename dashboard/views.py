from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from opportunities.models import Opportunity
from applications.models import Application
from dashboard.ai_recommendation import recommend_opportunities


@login_required
def dashboard_view(request):

    # Agency / Supervisor Dashboard
    if request.user.is_staff or getattr(request.user, "role", "") == "supervisor":
        opportunities = Opportunity.objects.all()
        applications = Application.objects.all()

        context = {
            "opportunities": opportunities,
            "applications": applications,
            "total_opportunities": opportunities.count(),
            "total_applications": applications.count(),
            "pending_applications": applications.filter(status="pending").count(),
        }

        return render(request, "dashboard/agency_dashboard.html", context)

    # Student / User Dashboard
    opportunities = Opportunity.objects.filter(is_active=True)

    total_opportunities = opportunities.count()

    total_applications = Application.objects.filter(
        student=request.user
    ).count()

    total_hours = Application.objects.filter(
        student=request.user,
        status="completed"
    ).aggregate(
        total=Sum("volunteer_hours")
    )["total"] or 0

    user_data = {
        "major": getattr(request.user, "major", "") or "",
        "interests": getattr(request.user, "interests", "") or "",
    }

    recommended = recommend_opportunities(user_data, opportunities)

    context = {
        "total_opportunities": total_opportunities,
        "total_applications": total_applications,
        "total_hours": total_hours,
        "recommended": recommended,
    }

    return render(request, "dashboard/dashboard.html", context)