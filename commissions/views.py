from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CommissionForm, JobApplicationForm, JobFormSet
from .models import Commission, Job, JobApplication
from .services import CommissionService

service = CommissionService()


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'
    context_object_name = 'commissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        status_order = {
            'Open': 0,
            'Full': 1,
            'Completed': 2,
            'Discontinued': 3,
        }

        def sort_commissions(queryset):
            return sorted(
                queryset,
                key=lambda c: (status_order.get(c.status, 99), -c.created_on.timestamp())
            )

        all_commissions = Commission.objects.all()

        if user.is_authenticated:
            user_profile = user.profile
            created = all_commissions.filter(maker=user_profile)
            applied_ids = JobApplication.objects.filter(
                applicant=user_profile
            ).values_list('job__commission__id', flat=True)
            applied = all_commissions.filter(
                id__in=applied_ids
            ).exclude(maker=user_profile)
            all_commissions = all_commissions.exclude(
                id__in=created
            ).exclude(id__in=applied)
            context['created_commissions'] = sort_commissions(created)
            context['applied_commissions'] = sort_commissions(applied)

        context['commissions'] = sort_commissions(all_commissions)
        return context


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'
    context_object_name = 'commission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        summary = service.get_commission_summary(commission)
        context['total_manpower'] = summary['total_manpower']
        context['open_manpower'] = summary['open_manpower']

        jobs_with_counts = []
        for job in commission.jobs.all():
            accepted_count = job.applications.filter(
                status=JobApplication.Status.ACCEPTED
            ).count()
            jobs_with_counts.append({
                'job': job,
                'accepted_count': accepted_count,
                'is_full': accepted_count >= job.manpower_required,
            })

        context['jobs_with_counts'] = jobs_with_counts
        context['job_application_form'] = JobApplicationForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        commission = self.get_object()
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        try:
            service.apply_to_job(
                applicant=request.user.profile,
                job=job,
            )
        except ValueError:
            pass

        return redirect('commissions:commission_detail', pk=commission.pk)
    

class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role != 'Commission Maker':
                return HttpResponseForbidden(
                    "You must be a Commission Maker to create commissions."
                )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(self.request.POST)
        else:
            context['job_formset'] = JobFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']

        if not job_formset.is_valid():
            return self.form_invalid(form)

        jobs_data = [
            f.cleaned_data for f in job_formset
            if f.cleaned_data and not f.cleaned_data.get('DELETE')
        ]

        commission = service.create_commission(
            author=self.request.user.profile,
            data=form.cleaned_data,
            jobs_data=jobs_data,
        )
        return redirect('commissions:commission_detail', pk=commission.pk)


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role != 'Commission Maker':
                return HttpResponseForbidden(
                    "You must be a Commission Maker to update commissions."
                )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['job_formset'] = JobFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']

        if not job_formset.is_valid():
            return self.form_invalid(form)

        commission = form.save(commit=False)
        commission.save()
        job_formset.save()
        service.sync_commission_status(commission)
        return redirect('commissions:commission_detail', pk=commission.pk)