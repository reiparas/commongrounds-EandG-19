from django.contrib import admin
from .models import ProjectCategory, Project, Favorite, ProjectReview, ProjectRating
# Register your models here.

class FavoriteInLine(admin.StackedInline):
    model = Favorite
    can_delete = True

class ProjectReviewInLine(admin.StackedInline):
    model = ProjectReview
    can_delete = True

class ProjectRatingInLine(admin.StackedInline):
    model = ProjectRating
    can_delete = True

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = [FavoriteInLine, ProjectReviewInLine, ProjectRatingInLine,]

admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)