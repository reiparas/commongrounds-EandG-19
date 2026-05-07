from django import forms
from .models import Project, Favorite, ProjectReview, ProjectRating

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'category', 'description', 'materials', 'steps',)

class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ('project_Status',)

class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ('score',)

class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ('comment', 'review_Image',)