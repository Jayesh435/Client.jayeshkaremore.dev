from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from .models import Payment
from projects.models import Project
from accounts.models import Client


def get_client_projects(user):
    try:
        return user.client_profile.projects.all()
    except Client.DoesNotExist:
        return Project.objects.none()


@login_required
def payment_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all().select_related('client__user')
        payments = Payment.objects.all().select_related('project__client__user')
    else:
        projects = get_client_projects(request.user)
        payments = Payment.objects.filter(project__in=projects)

    projects = projects.annotate(
        amount_paid_calc=Coalesce(Sum('payments__amount'), 0, output_field=DecimalField(max_digits=10, decimal_places=2)),
        remaining_balance_calc=F('total_cost') - Coalesce(Sum('payments__amount'), 0, output_field=DecimalField(max_digits=10, decimal_places=2)),
    )

    return render(request, 'payments/payment_list.html', {
        'projects': projects,
        'payments': payments,
    })


@login_required
def payment_detail(request, project_id):
    if request.user.is_superuser:
        project = get_object_or_404(Project, pk=project_id)
    else:
        projects = get_client_projects(request.user)
        project = get_object_or_404(projects, pk=project_id)

    payments = project.payments.all()
    amount_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
    remaining_balance = project.total_cost - amount_paid

    return render(request, 'payments/payment_detail.html', {
        'project': project,
        'payments': payments,
        'amount_paid': amount_paid,
        'remaining_balance': remaining_balance,
    })
