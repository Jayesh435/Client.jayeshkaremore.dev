from django.db import models
from accounts.models import Client


class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('revision', 'Revision'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress_percentage = models.IntegerField(default=0)
    live_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

    @property
    def remaining_balance(self):
        return self.total_cost - self.amount_paid

    @property
    def days_remaining(self):
        from datetime import date
        if self.deadline:
            delta = self.deadline - date.today()
            return delta.days
        return None

    class Meta:
        ordering = ['-created_at']


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['is_completed', '-created_at']


class FileUpload(models.Model):
    UPLOADER_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='project_files/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_by = models.CharField(max_length=10, choices=UPLOADER_CHOICES, default='client')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.project_name} - {self.file.name}"

    @property
    def filename(self):
        import os
        return os.path.basename(self.file.name)

    class Meta:
        ordering = ['-uploaded_at']
