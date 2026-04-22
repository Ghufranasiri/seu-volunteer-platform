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