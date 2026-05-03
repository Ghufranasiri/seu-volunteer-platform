from django.shortcuts import render

from .models import Notification

def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/notifications.html', {'notifications': notifications})
