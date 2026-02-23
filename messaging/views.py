from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Message
from .forms import MessageForm
from projects.models import Project
from accounts.models import Client


def get_client_projects(user):
    try:
        return user.client_profile.projects.all()
    except Client.DoesNotExist:
        return Project.objects.none()


@login_required
def message_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all().select_related('client__user')
    else:
        projects = get_client_projects(request.user)

    project_id = request.GET.get('project')
    if project_id:
        if request.user.is_superuser:
            project = get_object_or_404(Project, pk=project_id)
        else:
            project = get_object_or_404(projects, pk=project_id)
        msgs = project.messages.all().select_related('sender')
    else:
        project = projects.first()
        msgs = project.messages.all().select_related('sender') if project else Message.objects.none()

    form = MessageForm()
    if request.method == 'POST' and project:
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.project = project
            msg.sender = request.user
            msg.save()
            return redirect(f'/messages/?project={project.id}')

    return render(request, 'messaging/message_list.html', {
        'projects': projects,
        'selected_project': project,
        'messages': msgs,
        'form': form,
    })
