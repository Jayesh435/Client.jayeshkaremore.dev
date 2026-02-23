from django.contrib import admin
from .models import Project, Task, FileUpload


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


class FileUploadInline(admin.TabularInline):
    model = FileUpload
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'client', 'status', 'progress_percentage', 'deadline', 'total_cost', 'amount_paid']
    list_filter = ['status', 'created_at']
    search_fields = ['project_name', 'client__user__username', 'client__company_name']
    inlines = [TaskInline, FileUploadInline]
    list_editable = ['status', 'progress_percentage']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['project', 'description', 'uploaded_by', 'uploaded_at']
    list_filter = ['uploaded_by', 'uploaded_at']
