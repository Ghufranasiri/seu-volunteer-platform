def opportunity_list(request):
    opportunities = Opportunity.objects.all().order_by('-created_at')
    return render(request, 'opportunities/opportunity_list.html', {
        'opportunities': opportunities
    })