from django.shortcuts import render
from .ai_recommendation import recommend_opportunities


def dashboard_view(request):
    opportunities = [
        {
            "title": "Teaching Kids",
            "category": "education"
        },
        {
            "title": "Hospital Volunteer",
            "category": "health"
        },
        {
            "title": "Event Organizer",
            "category": "management"
        }
    ]

    user = {
        "major": "education",
        "interests": ["teaching"]
    }

    recommended = recommend_opportunities(user, opportunities)

    context = {
        "total_opportunities": 10,
        "total_applications": 25,
        "total_hours": 120,
        "recommended": recommended
    }

    return render(request, "dashboard/dashboard.html", context)
