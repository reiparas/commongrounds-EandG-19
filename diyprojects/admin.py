from django.contrib import admin
from .models import ProjectCategory, Project
# Register your models here.

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory

class ProjectAdmin(admin.ModelAdmin):
    model = Project

admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)