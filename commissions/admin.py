from django.contrib import admin
from .models import Commission, CommissionType, Job, JobApplication


class JobInLine(admin.TabularInline):
    model = Job
    extra = 1

class JobApplicationInLine(admin.TabularInline):
    model = JobApplication
    extra = 1

@admin.register(CommissionType)
class CommissionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'maker', 'commission_type', 'status', 'created_on']
    list_filter = ['status', 'commission_type']
    inlines = [JobInLine]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['role', 'commission', 'manpower_required', 'status']
    list_filter = ['status']
    inlines = [JobApplicationInLine]

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'status', 'applied_on']
    list_filter = ['status']
