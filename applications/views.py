from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from opportunities.models import Opportunity
from .models import Application


@login_required
def apply_opportunity(request, pk):
    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        is_active=True,
        status='approved'
    )

    if request.user.role != 'student':
        messages.error(
            request,
            "Only students can apply for volunteer opportunities."
        )
        return redirect('opportunities:opportunity_list')

    existing_application = Application.objects.filter(
        student=request.user,
        opportunity=opportunity
    ).first()

    if existing_application:
        messages.info(
            request,
            "You have already applied for this opportunity."
        )
        return redirect('dashboard:student_dashboard')

    if request.method == "POST":
        Application.objects.create(
            student=request.user,
            opportunity=opportunity,
            status='pending'
        )

        messages.success(
            request,
            "Your application has been submitted successfully."
        )

        return redirect('dashboard:student_dashboard')

    return render(request, "applications/apply.html", {
        "opportunity": opportunity,
    })

