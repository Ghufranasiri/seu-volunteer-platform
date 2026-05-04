from django.shortcuts import render, redirect, get_object_or_404
from .models import Opportunity


def opportunity_list(request):
    opportunities = Opportunity.objects.all()
    return render(request, "opportunities/opportunity_list.html", {
        "opportunities": opportunities
    })


def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, "opportunities/opportunity_detail.html", {
        "opportunity": opportunity
    })


# ✅ CREATE
def create_opportunity(request):
    if request.method == "POST":
        Opportunity.objects.create(
            name=request.POST.get("title"),
            description=request.POST.get("description"),
            location=request.POST.get("location"),
            date=request.POST.get("date"),
            hours=request.POST.get("hours") or 1,
            organization=request.POST.get("organization") or "SEU Volunteer Agency",
        )
        return redirect("dashboard")

    return render(request, "opportunities/create_opportunity.html")


# ✅ EDIT
def edit_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    if request.method == "POST":
        opportunity.name = request.POST.get("name")
        opportunity.description = request.POST.get("description")
        opportunity.location = request.POST.get("location")
        opportunity.date = request.POST.get("date")
        opportunity.hours = request.POST.get("hours") or 1
        opportunity.organization = request.POST.get("organization")

        opportunity.save()
        return redirect("dashboard")

    return render(request, "opportunities/edit_opportunity.html", {
        "opportunity": opportunity
    })


# ✅ DELETE
def delete_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)

    if request.method == "POST":
        opportunity.delete()

    return redirect("dashboard")