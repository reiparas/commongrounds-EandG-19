from django.shortcuts import render
from django.http import HttpResponse
from .models import ProjectCategory, Project

# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    ctx = {
        'projects': projects
    }
    return render(request, "diyprojects/list.html", ctx)

def project_detail(request, id):
    ctx = {
        'project': Project.objects.get(pk=id)
    }
    return render(request, "diyprojects/project.html", ctx)