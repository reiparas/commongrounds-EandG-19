from django.db import models
from django.urls import reverse
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