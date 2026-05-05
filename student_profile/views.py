from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm

@login_required
def profile_view(request):
    return render(request, 'student_profile/profile.html')

@login_required
def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'student_profile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })