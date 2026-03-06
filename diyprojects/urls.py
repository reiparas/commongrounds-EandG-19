from django.urls import path
from .views import project_list, project_detail

urlpatterns = [
    path('projects', project_list, name='project_list'),
    path('project<int:id>', project_detail, name='project_detail')
]

app_name = "diyprojects"