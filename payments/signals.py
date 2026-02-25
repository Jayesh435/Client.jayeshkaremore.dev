from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db.models import Sum

from .models import Payment


def _sync_project_amount_paid(project):
    total_paid = project.payments.aggregate(total=Sum('amount'))['total'] or 0
    project.amount_paid = total_paid
    project.save(update_fields=['amount_paid'])


@receiver(post_save, sender=Payment)
def sync_project_amount_paid_on_save(sender, instance, **kwargs):
    _sync_project_amount_paid(instance.project)


@receiver(post_delete, sender=Payment)
def sync_project_amount_paid_on_delete(sender, instance, **kwargs):
    _sync_project_amount_paid(instance.project)
