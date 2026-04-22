from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# --- 1. دالة تسجيل الدخول ---
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # سيوجهك للدالة بالأسفل
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'registration/login.html')
            
    return render(request, 'registration/login.html')

# --- 2. دالة تسجيل الخروج ---
def logout_view(request):
    logout(request)
    return redirect('home')

# --- 3. الصفحات العامة ---
def home(request):
    context = {
        'total_volunteers': 2547,
        'total_opportunities': 456,
        'total_hours': 51200,
        'total_organizations': 127,
    }
    return render(request, 'home.html', context)

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'registration/signup.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'registration/signup.html')

# --- 4. لوحات التحكم (تعديل المسارات بناءً على الصور) ---

@login_required
def admin_dashboard(request):
    context = {
        'total_volunteers': User.objects.count(),
        'total_organizations': 127,
        'active_opportunities': 456,
    }
    # تم التعديل ليطابق المسار: dashboard/templates/dashboard/dashboard.html
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def manage_users(request):
    users_list = User.objects.all()
    # تم التعديل ليطابق المسار: dashboard/templates/dashboard/manage_users.html
    return render(request, 'dashboard/manage_users.html', {'users': users_list})

@login_required
def add_opportunity(request):
    if request.method == 'POST':
        return redirect('dashboard')
    return render(request, 'dashboard/add_opportunity.html')

# --- 5. الفرص التطوعية ---
def opportunities_list(request):
    return render(request, 'opportunities.html', {'opportunities': []})

def opportunity_detail(request, pk):
    return render(request, 'opportunity_detail.html', {'id': pk})

@login_required
def student_dashboard(request): 
    return render(request, 'dashboard/student_dashboard.html')

@login_required
def agency_dashboard(request): 
    return render(request, 'dashboard/agency_dashboard.html')