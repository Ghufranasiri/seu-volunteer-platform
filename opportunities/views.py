from django.shortcuts import render, get_object_or_404
from .models import Opportunity


def opportunity_list(request):
    opportunities = Opportunity.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'opportunities/opportunity_list.html', {
        'opportunities': opportunities
    })


def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, is_active=True)
    return render(request, 'opportunities/opportunity_detail.html', {
        'opportunity': opportunity
    })
