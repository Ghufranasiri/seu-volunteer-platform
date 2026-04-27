from django.shortcuts import render
from .ai_recommendation import recommend_opportunities

def dashboard_view(request):
    # Example user data 
    user = {
    "major": "Education",
    "interests": ["teaching", "technology"]
}

    # Temporary opportunities 
    opportunities = []

    recommended = recommend_opportunities(user, opportunities)

    context = {
        "total_opportunities": 10,
        "total_applications": 25,
        "total_hours": 120,
        "recommended": recommended
    }

    return render(request, "dashboard/dashboard.html", context)
