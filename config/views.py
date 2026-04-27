from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# نماذج بسيطة - سيتم استبدالها بـ models حقيقية لاحقاً
def home(request):
    """الصفحة الرئيسية"""
    context = {
        'total_volunteers': 2547,
        'total_opportunities': 456,
        'total_hours': 51200,
        'total_organizations': 127,
    }
    return render(request, 'home.html', context)

def logout_view(request):
    """Logs out current user and redirects home"""
    logout(request)
    messages.info(request, 'تم تسجيل الخروج.')
    return redirect('home')

from django.contrib.auth import authenticate, logout

def login_view(request):
    """صفحة تسجيل الدخول، يعالج POST للتوثيق"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"[DEBUG] login POST email={email!r} password={'*' * len(password or '')}")
        user = authenticate(request, username=email, password=password)
        print(f"[DEBUG] authenticate returned: {user}")
        if user is not None:
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح.')
            return redirect('home')
        else:
            messages.error(request, 'البريد الإلكتروني أو كلمة المرور غير صحيحة.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def register_view(request):
    """صفحة التسجيل - يعالج الـ POST لإنشاء مستخدم جديد"""
    if request.method == 'POST':
        # gather basic info
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        university_id = request.POST.get('university_id', '').strip()
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        raw_role = request.POST.get('role', 'student')

        # default username to email if not provided
        username = email or None

        # normalize role values used in model
        if raw_role == 'agency':
            role = 'supervisor'
        else:
            role = 'student'

        # basic validation
        if not email or not password or not first_name or not last_name:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
            return render(request, 'register.html')

        if password != confirm:
            messages.error(request, 'كلمة المرور وتأكيدها غير متطابقين.')
            return render(request, 'register.html')

        User = get_user_model()
        if username and User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم موجود مسبقاً.')
            return render(request, 'register.html')
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'البريد الإلكتروني مستخدم بالفعل.')
            return render(request, 'register.html')

        # create user and fill extras
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.university_id = university_id
        user.role = role
        user.save()
        login(request, user)
        messages.success(request, 'تم إنشاء الحساب بنجاح.')
        return redirect('home')

    return render(request, 'register.html')

def opportunities_list(request):
    """قائمة الفرص التطوعية"""
    # بيانات نموذجية - سيتم استبدالها بـ database queries
    opportunities = [
        {
            'id': 1,
            'title': 'تدريس الرياضيات للطلاب',
            'organization': 'جمعية التعليم',
            'category': 'التعليم',
            'difficulty': 'سهل',
            'hours': 10,
            'registrations': 12,
            'max_registrations': 20,
            'date_start': '2026-03-15',
        },
        {
            'id': 2,
            'title': 'مساعدة طبية - عيادة صحية',
            'organization': 'الهلال الأحمر',
            'category': 'الصحة',
            'difficulty': 'وسط',
            'hours': 20,
            'registrations': 8,
            'max_registrations': 15,
            'date_start': '2026-03-20',
        },
        {
            'id': 3,
            'title': 'تنظيف الحديقة العامة',
            'organization': 'جمعية البيئة',
            'category': 'البيئة',
            'difficulty': 'سهل',
            'hours': 8,
            'registrations': 25,
            'max_registrations': 30,
            'date_start': '2026-03-18',
        },
    ]
    context = {
        'opportunities': opportunities,
        'total_count': len(opportunities),
    }
    return render(request, 'opportunities.html', context)

def opportunity_detail(request, pk):
    """تفاصيل فرصة واحدة"""
    # بيانات نموذجية
    opportunity = {
        'id': pk,
        'title': 'تدريس الرياضيات للطلاب',
        'organization': 'جمعية التعليم',
        'category': 'التعليم',
        'difficulty': 'سهل',
        'hours': 10,
        'registrations': 12,
        'max_registrations': 20,
        'rating': 4.5,
        'reviews_count': 23,
        'description': 'فرصة تطوعية مميزة لدعم الطلاب في دراسة الرياضيات',
        'requirements': ['القدرة على التدريس', 'الصبر', 'التواصل الجيد'],
    }
    context = {
        'opportunity': opportunity,
    }
    return render(request, 'opportunity_detail.html', context)

@login_required
def student_dashboard(request):
    """لوحة تحكم الطالب"""
    context = {
        'total_hours': 42,
        'active_events': 3,
        'certificates': 2,
        'impact_score': 85,
        'recent_hours': 8,
    }
    return render(request, 'dashboard_student.html', context)

@login_required
def hours_tracking(request):
    """تتبع ساعات التطوع"""
    hours_data = [
        {'event': 'تدريس الرياضيات', 'organization': 'جمعية التعليم', 'category': 'التعليم', 'date': '2026-03-01', 'hours': 5, 'status': 'معتمد'},
        {'event': 'تنظيف الحديقة', 'organization': 'جمعية البيئة', 'category': 'البيئة', 'date': '2026-03-05', 'hours': 3, 'status': 'قيد الانتظار'},
    ]
    context = {
        'hours_data': hours_data,
        'total_hours': 42,
        'approved_hours': 35,
        'pending_hours': 7,
    }
    return render(request, 'hours.html', context)

@login_required
def certificates_view(request):
    """إدارة الشهادات"""
    certificates = [
        {'title': 'شهادة التميز التعليمي', 'hours': 15, 'organization': 'جمعية التعليم', 'date': '2026-02-15'},
        {'title': 'شهادة البطل الصحي', 'hours': 20, 'organization': 'الهلال الأحمر', 'date': '2026-02-20'},
    ]
    context = {
        'certificates': certificates,
        'total_certificates': len(certificates),
    }
    return render(request, 'certificates.html', context)

@login_required
def agency_dashboard(request):
    """لوحة تحكم المنظمة"""
    context = {
        'active_opportunities': 12,
        'total_registrations': 287,
        'total_hours': 5200,
        'approval_rate': 94,
    }
    return render(request, 'dashboard_agency.html', context)

@login_required
def admin_dashboard(request):
    """لوحة تحكم المسؤول"""
    context = {
        'total_volunteers': 2547,
        'active_opportunities': 456,
        'total_hours': 51200,
        'total_organizations': 127,
    }
    return render(request, 'dashboard_admin.html', context)