from django.db import models
from accounts.models import Profile


class CommissionType(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Commission(models.Model):

    class Status(models.TextChoices):
        OPEN = 'Open'
        FULL = 'Full'
        COMPLETED = 'Completed'
        Discontinued = 'Discontinued'

    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='Commission'
    )
    maker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='commissions',
        null=True
    )
    people_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title


class Job(models.Model):

    class Status(models.TextChoices):
        OPEN = 'Open'
        FULL = 'Full'
    
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.OPEN
    )
    
    class Meta:
        ordering = [
            'status',
            '-manpower_required',
            'role'
        ]
    
    def __str__(self):
        return self.role

class JobApplication(models.Model):

    class Status(models.TextChoices):
        PENDING = 'Pending'
        ACCEPTED = 'Accepted'
        REJECTED = 'Rejected'
    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            'status', 
            '-applied_on'
        ]
    
    def __str__(self):
        return f"{self.applicant} - {self.job}"