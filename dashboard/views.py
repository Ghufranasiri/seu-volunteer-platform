from django.shortcuts import render
from .ai_recommendation import recommend_opportunities
<<<<<<< HEAD

def dashboard_view(request):
    # Example user data 
    user = {
    "major": "Education",
    "interests": ["teaching", "technology"]
}

    # Temporary opportunities 
    opportunities = []
=======


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
>>>>>>> d3b871f (fix dashboard recommendation display)

    recommended = recommend_opportunities(user, opportunities)

    context = {
        "total_opportunities": 10,
        "total_applications": 25,
        "total_hours": 120,
        "recommended": recommended
    }

<<<<<<< HEAD
    return render(request, "dashboard/dashboard.html", context)
=======
    return render(request, "dashboard/dashboard.html", context)
>>>>>>> d3b871f (fix dashboard recommendation display)
