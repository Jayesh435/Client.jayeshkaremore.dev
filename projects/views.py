from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from .models import Project, Task, FileUpload
from .forms import FileUploadForm
from accounts.models import Client


def get_client_projects(user):
    try:
        return user.client_profile.projects.all()
    except Client.DoesNotExist:
        return Project.objects.none()


@login_required
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all().select_related('client__user')
    else:
        projects = get_client_projects(request.user)

    projects = projects.annotate(
        amount_paid_calc=Coalesce(Sum('payments__amount'), 0, output_field=DecimalField(max_digits=10, decimal_places=2)),
        remaining_balance_calc=F('total_cost') - Coalesce(Sum('payments__amount'), 0, output_field=DecimalField(max_digits=10, decimal_places=2)),
    )

    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)

    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'status_filter': status_filter,
        'status_choices': Project.STATUS_CHOICES,
    })


@login_required
def project_detail(request, pk):
    if request.user.is_superuser:
        project = get_object_or_404(Project, pk=pk)
    else:
        projects = get_client_projects(request.user)
        project = get_object_or_404(projects, pk=pk)

    tasks = project.tasks.all()
    files = project.files.all()
    amount_paid = project.payments.aggregate(total=Sum('amount'))['total'] or 0
    remaining_balance = project.total_cost - amount_paid
    upload_form = FileUploadForm()

    if request.method == 'POST':
        upload_form = FileUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            file_upload = upload_form.save(commit=False)
            file_upload.project = project
            file_upload.uploaded_by = 'admin' if request.user.is_superuser else 'client'
            file_upload.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('project_detail', pk=pk)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'files': files,
        'upload_form': upload_form,
        'amount_paid': amount_paid,
        'remaining_balance': remaining_balance,
    })


@login_required
def task_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = get_client_projects(request.user)

    project_id = request.GET.get('project')
    if project_id:
        project = get_object_or_404(projects, pk=project_id)
        tasks = project.tasks.all()
    else:
        tasks = Task.objects.filter(project__in=projects)
        project = None

    return render(request, 'projects/task_list.html', {
        'tasks': tasks,
        'projects': projects,
        'selected_project': project,
    })
