from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        app_label = 'diyprojects'

class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name='project',
        null=True)
    creator = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.SET_NULL,
        related_name='projects',
        null=True)
    description = models.TextField(blank=True)
    materials = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    created_On = models.DateTimeField(auto_now_add=True)
    updated_On = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('diyprojects:project_detail', kwargs={'id' : self.pk})

    class Meta:
        ordering = ['-created_On']
        app_label = 'diyprojects'

class Favorite(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='fav_projects'
    )
    date_Favorited = models.DateField(auto_now_add=True)
    PROJECT_STATUS_CHOICES = {
        'SL': 'Select',
        'BL': 'Backlog',
        'TD': 'To-Do',
        'DO': 'Done'
    }
    project_Status = models.CharField(
        max_length=2,
        choices=PROJECT_STATUS_CHOICES,
        default='SL'
    )

class ProjectReview(models.Model):
    reviewer = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='rev_projects'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='reviewer'
    )
    comment = models.TextField(blank=True)
    review_Image = models.ImageField(upload_to='images/diyprojects/', null=True)

class ProjectRating(models.Model):
    rater = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='rate_projects'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='rater'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )