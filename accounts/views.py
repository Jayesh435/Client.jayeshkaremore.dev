from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client
from .forms import ProfileUpdateForm


@login_required
def profile(request):
    try:
        client = request.user.client_profile
    except Client.DoesNotExist:
        client = None

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=client, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=client, user=request.user)

    return render(request, 'accounts/profile.html', {'form': form, 'client': client})
