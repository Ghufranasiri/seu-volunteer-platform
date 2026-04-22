from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Certificate
from accounts.models import Notification

@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user).order_by('-issued_at')
    notifications_count = Notification.objects.filter(user=request.user).count()

    return render(request, 'users/my_certificates.html', {
        'certificates': certificates,
        'notifications_count': notifications_count,
    })


from .models import Certificate


def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    return render(request, 'users/certificate_detail.html', {'certificate': certificate})


def certificate_detail_ar(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    return render(request, 'users/certificate_detail_ar.html', {'certificate': certificate})


@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user).order_by('-issued_at')
    return render(request, 'users/my_certificates.html', {'certificates': certificates})