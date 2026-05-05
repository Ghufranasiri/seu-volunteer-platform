from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from opportunities.models import Opportunity
from applications.models import Application
from dashboard.ai_recommendation import recommend_opportunities


@login_required
def dashboard_view(request):

    # 🔒 منع دخول الأدمن للداشبورد
    if request.user.is_staff:
        return redirect('/admin/')

    # 📊 الفرص المتاحة
    opportunities = Opportunity.objects.filter(is_active=True)

    total_opportunities = opportunities.count()

    # 📄 عدد التقديمات
    total_applications = Application.objects.filter(
        student=request.user
    ).count()

    # ⏱️ مجموع الساعات
    total_hours = Application.objects.filter(
        student=request.user,
        status='completed'
    ).aggregate(
        total=Sum('volunteer_hours')
    )['total'] or 0

    
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