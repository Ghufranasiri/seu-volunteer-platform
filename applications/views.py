from django.shortcuts import render, get_object_or_404
from opportunities.models import Opportunity


def apply_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    if request.method == "POST":
        context = {
            "opportunity": opportunity,
            "success": True,
        }
        return render(request, "applications/apply.html", context)

    context = {
        "opportunity": opportunity,
    }
    return render(request, "applications/apply.html", context)