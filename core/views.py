from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from projects.models import Project
from accounts.models import Client


@login_required
def home(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    if request.user.is_superuser:
        projects = Project.objects.all().select_related('client__user')
        context = {
            'projects': projects,
            'total_clients': Client.objects.count(),
            'total_projects': projects.count(),
            'completed_projects': projects.filter(status='completed').count(),
            'in_progress_projects': projects.filter(status='in_progress').count(),
        }
        return render(request, 'core/admin_dashboard.html', context)

    try:
        client = request.user.client_profile
    except Client.DoesNotExist:
        return render(request, 'core/no_profile.html')

    projects = client.projects.all()
    context = {
        'client': client,
        'projects': projects,
        'active_project': projects.filter(status='in_progress').first() or projects.first(),
    }
    return render(request, 'core/dashboard.html', context)
