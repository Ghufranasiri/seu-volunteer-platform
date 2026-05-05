from django.shortcuts import render



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model

User = get_user_model()


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('opportunity_list')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not email or email.strip() == "":
            messages.error(request, 'Email is required.')
            return render(request, 'registration/signup.html')

        email = email.strip()

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'registration/signup.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.first_name = first_name or ""
        user.save()

        login(request, user)
        return redirect('opportunity_list')

    return render(request, 'registration/signup.html')


def dashboard(request):
    return redirect('opportunity_list')


def student_dashboard(request):
    return redirect('opportunity_list')


def agency_dashboard(request):
    return redirect('opportunity_list')


def admin_dashboard(request):
    return redirect('opportunity_list')


def add_opportunity(request):
    return redirect('opportunity_list')


def view_volunteers(request):
    return redirect('opportunity_list')


def manage_users(request):
    return redirect('opportunity_list')


def approve_hours(request):
    return redirect('opportunity_list')

from django.shortcuts import render
from .ai_recommendation import recommend_opportunities

from django.shortcuts import render, redirect

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

    return render(request, "dashboard/dashboard.html", context)

