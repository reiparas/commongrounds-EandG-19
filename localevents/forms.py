from django import forms
from .models import Event, EventSignup

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'category',
            'event_image',
            'description',
            'location',
            'start_time',
            'end_time',
            'event_capacity',
            'status',
        ]
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']

class EventSignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['new_registrant']
        labels = {'new_registrant': 'Your Name'}
        widgets = {
            'new_registrant': forms.TextInput(
                attrs={'placeholder': 'Enter your name'}
            ),
        }
