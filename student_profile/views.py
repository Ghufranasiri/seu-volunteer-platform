from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from .models import Profile


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'student_profile/profile.html', {
        'profile': profile
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'student_profile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })