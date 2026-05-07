from django.db import transaction

from .models import Commission, Job, JobApplication


class CommissionService:

    def create_commission(self, author, data, jobs_data):
        with transaction.atomic():
            commission = Commission.objects.create(
                title=data['title'],
                description=data['description'],
                commission_type=data.get('commission_type'),
                maker=author,
                people_required=data['people_required'],
                status=data.get('status', Commission.Status.OPEN),
            )
            for job_data in jobs_data:
                Job.objects.create(
                    commission=commission,
                    role=job_data['role'],
                    manpower_required=job_data['manpower_required'],
                    status=job_data.get('status', Job.Status.OPEN),
                )
            return commission

    def apply_to_job(self, applicant, job):
        already_applied = JobApplication.objects.filter(
            job=job,
            applicant=applicant
        ).exists()
        if already_applied:
            raise ValueError("You have already applied to this job.")

        accepted_count = JobApplication.objects.filter(
            job=job,
            status=JobApplication.Status.ACCEPTED
        ).count()
        if accepted_count >= job.manpower_required:
            raise ValueError("This job is already full.")

        application = JobApplication.objects.create(
            job=job,
            applicant=applicant,
            status=JobApplication.Status.PENDING,
        )
        return application

    def sync_commission_status(self, commission):
        jobs = commission.jobs.all()
        if jobs.exists() and all(
            job.status == Job.Status.FULL for job in jobs
        ):
            commission.status = Commission.Status.FULL
            commission.save()

    def get_commission_summary(self, commission):
        jobs = commission.jobs.all()
        total_manpower = sum(job.manpower_required for job in jobs)
        accepted_count = sum(
            job.applications.filter(
                status=JobApplication.Status.ACCEPTED
            ).count()
            for job in jobs
        )
        open_manpower = total_manpower - accepted_count
        return {
            'total_manpower': total_manpower,
            'open_manpower': open_manpower,
        }