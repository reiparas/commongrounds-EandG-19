from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from .models import ProjectCategory, Project, Favorite, ProjectReview, ProjectRating
from .forms import ProjectForm, FavoriteForm, ProjectReviewForm, ProjectRatingForm
from accounts.models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    currentUser = request.user
    if currentUser.is_authenticated:
        currentProfile = currentUser.profile
        createdProjects = currentProfile.projects.all()
        favProjects = Project.objects.filter(profile__profile=currentProfile)
        revProjects = Project.objects.filter(reviewer__reviewer=currentProfile)
        ctx = {
            'projects': projects, 'createdProjects': createdProjects, 'favProjects': favProjects, 'revProjects': revProjects
        }
    else:
        ctx = {
            'projects': projects
        }
    return render(request, "diyprojects/list.html", ctx)

def project_detail(request, id):
    currentUser = request.user
    project = Project.objects.get(pk=id)
    ratings = ProjectRating.objects.filter(project=project)
    avgRating = ratings.aggregate(Avg('score'))['score__avg']
    favorites = Favorite.objects.filter(project=project)
    reviews = ProjectReview.objects.filter(project=project)
    if currentUser.is_authenticated:
        currentProfile = currentUser.profile
        ratProjects = Project.objects.filter(rater__rater=currentProfile)
        favProjects = Project.objects.filter(profile__profile=currentProfile)
        revProjects = Project.objects.filter(reviewer__reviewer=currentProfile)
        rateForm = ProjectRatingForm()
        favForm = FavoriteForm()
        revForm = ProjectReviewForm()
        if request.method == 'POST':
            if 'addRate' in request.POST:
                rateForm = ProjectRatingForm(request.POST)
                if rateForm.is_valid():
                    rate = rateForm.save(commit=False)
                    rate.project = project
                    rate.rater = currentProfile
                    rate.save()
            elif 'changeRate' in request.POST:
                rateForm = ProjectRatingForm(request.POST, instance = ratings.get(rater=currentProfile))
                if rateForm.is_valid():
                    rate = rateForm.save()
            elif 'removeRate' in request.POST:
                rateToRemove = ratings.get(rater=currentProfile)
                rateToRemove.delete()
            elif 'addFav' in request.POST:
                favForm = FavoriteForm(request.POST)
                if favForm.is_valid():
                    fave = favForm.save(commit=False)
                    fave.project = project
                    fave.profile = currentProfile
                    fave.save()
            elif 'changeStat' in request.POST:
                favForm = FavoriteForm(request.POST, instance = favorites.get(profile=currentProfile))
                if favForm.is_valid():
                    fave = favForm.save()
            elif 'removeFave' in request.POST:
                faveToRemove = favorites.get(profile=currentProfile)
                faveToRemove.delete()
            elif 'addRev' in request.POST:
                revForm = ProjectReviewForm(request.POST, request.FILES)
                if revForm.is_valid():
                    rev = revForm.save(commit=False)
                    rev.project = project
                    rev.reviewer = currentProfile
                    rev.save()
            elif 'changeRev' in request.POST:
                revForm = ProjectReviewForm(request.POST, request.FILES, instance = reviews.get(reviewer=currentProfile))
                if revForm.is_valid():
                    rev = revForm.save()
            elif 'removeRev' in request.POST:
                revToRemove = reviews.get(reviewer=currentProfile)
                revToRemove.delete()
            return redirect('diyprojects:project_detail', id = project.pk)
        ctx = {
            'project': project, 'avgRating': avgRating, 'ratings': ratings, 'ratProjects': ratProjects, 'rateForm': rateForm, 'favorites': favorites, 'favProjects':favProjects, 'favForm': favForm, 'reviews': reviews, 'revProjects': revProjects, 'revForm':revForm
        }
    else:
        ctx = {
            'project': project, 'avgRating': avgRating, 'ratings': ratings, 'favorites': favorites,'reviews': reviews
        }

    return render(request, "diyprojects/project.html", ctx)

@login_required
def project_create(request):
    currentUser = request.user
    currentProfile = currentUser.profile
    projForm = ProjectForm()
    if request.method == 'POST':
        projForm = ProjectForm(request.POST)
        if projForm.is_valid():
            proj = projForm.save(commit=False)
            proj.creator = currentProfile
            proj.save()
            return redirect('diyprojects:project_detail', id = proj.pk)
    ctx = {
        'projForm': projForm
    }
    return render(request, "diyprojects/create.html", ctx)

@login_required
def project_update(request, id):
    project = Project.objects.get(pk=id)
    projForm = ProjectForm()
    if request.method == 'POST':
        projForm = ProjectForm(request.POST, instance = project)
        if projForm.is_valid():
            projForm.save()
            return redirect('diyprojects:project_detail', id = project.pk)
    ctx = {
        'project': project, 'projForm': projForm
    }
    return render(request, "diyprojects/update.html", ctx)