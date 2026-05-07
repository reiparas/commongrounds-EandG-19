from django import forms

from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):

    class Meta:
        model = Commission
        fields = [
            'title',
            'description',
            'commission_type',
            'people_required',
            'status',
        ]
        widgets = {
            'status': forms.Select(),
            'commission_type': forms.Select(),
        }


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            'role',
            'manpower_required',
            'status',
        ]
        widgets = {
            'status': forms.Select(),
        }


JobFormSet = forms.inlineformset_factory(
    Commission,
    Job,
    form=JobForm,
    extra=1,
    can_delete=True,
)


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = []