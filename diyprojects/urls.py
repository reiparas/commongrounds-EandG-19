from django.urls import path
from .views import project_list, project_detail, project_create, project_update

urlpatterns = [
    path('projects', project_list, name='project_list'),
    path('project/<int:id>', project_detail, name='project_detail'),
    path('project/add', project_create, name='project_create'),
    path('project/<int:id>/edit', project_update, name='project_update')
]

app_name = "diyprojects"