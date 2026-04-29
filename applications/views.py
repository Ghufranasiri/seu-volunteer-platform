from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

# دالة للتأكد أن المستخدم هو الأدمن فقط
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    # جلب كل المستخدمين واستبعاد الأدمن نفسه من القائمة
    all_users = User.objects.all().exclude(is_superuser=True)
    return render(request, 'dashboard/manage_users.html', {'users': all_users})