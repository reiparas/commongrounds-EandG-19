from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from .models import ProjectCategory, Project, Favorite, ProjectReview, ProjectRating
from .forms import FavoriteForm, ProjectReviewForm, ProjectRatingForm
from accounts.models import Profile

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
                    return redirect('diyprojects:project_detail', id = project.pk)
            elif 'changeRate' in request.POST:
                rateForm = ProjectRatingForm(request.POST, instance = ratings.get(rater=currentProfile))
                if rateForm.is_valid():
                    rate = rateForm.save()
                    return redirect('diyprojects:project_detail', id = project.pk)
            elif 'removeRate' in request.POST:
                rateToRemove = ratings.get(rater=currentProfile)
                rateToRemove.delete()
                return redirect('diyprojects:project_detail', id = project.pk)
            elif 'addFav' in request.POST:
                favForm = FavoriteForm(request.POST)
                if favForm.is_valid():
                    fave = favForm.save(commit=False)
                    fave.project = project
                    fave.profile = currentProfile
                    fave.save()
                    return redirect('diyprojects:project_detail', id = project.pk)
            elif 'changeStat' in request.POST:
                favForm = FavoriteForm(request.POST, instance = favorites.get(profile=currentProfile))
                if favForm.is_valid():
                    fave = favForm.save()
                    return redirect('diyprojects:project_detail', id = project.pk)
            elif 'removeFave' in request.POST:
                faveToRemove = favorites.get(profile=currentProfile)
                faveToRemove.delete()
                return redirect('diyprojects:project_detail', id = project.pk)
            elif 'addRev' in request.POST:
                revForm = ProjectReviewForm(request.POST, request.FILES)
                if revForm.is_valid():
                    rev = revForm.save(commit=False)
                    rev.project = project
                    rev.reviewer = currentProfile
                    rev.save()
                    return redirect('diyprojects:project_detail', id = project.pk)
            elif 'changeRev' in request.POST:
                revForm = ProjectReviewForm(request.POST, request.FILES, instance = reviews.get(reviewer=currentProfile))
                if revForm.is_valid():
                    rev = revForm.save()
                    return redirect('diyprojects:project_detail', id = project.pk)
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