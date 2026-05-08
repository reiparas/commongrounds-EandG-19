from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import EventForm, EventSignupForm
from .models import Event, EventSignup


class BaseSignupView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        user = request.user

        if self.check_capacity(event) and self.check_ownership(event, user):
            return self.handle_signup(request, event, user)
        return redirect(self.get_redirect_url(event))

    def check_capacity(self, event):
        return not event.is_full

    def check_ownership(self, event, user):
        if user.is_authenticated:
            return user.profile not in event.organizer.all()
        return True

    def handle_signup(self, request, event, user):
        raise NotImplementedError

    def get_redirect_url(self, event):
        return reverse('localevents:event_detail', kwargs={'pk': event.pk})

@method_decorator(login_required, name='post')
class EventSignupView(BaseSignupView):
    def handle_signup(self, request, event, user):
        EventSignup.objects.create(event=event, user_registrant=user.profile)
        return redirect(self.get_redirect_url(event))

class EventSignupFormView(View):
    template_name = 'localevents/event_signup.html'

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = EventSignupForm()
        return render(request, self.template_name, {'event': event, 'form': form})

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if event.is_full:
            return redirect(
                reverse('localevents:event_detail', kwargs={'pk': event.pk})
            )

        form = EventSignupForm(request.POST)
        if form.is_valid():
            signup = form.save(commit=False)
            signup.event = event
            signup.save()
            return redirect(
                reverse('localevents:event_detail', kwargs={'pk': event.pk})
            )

        return render(request, self.template_name, {'event': event, 'form': form})


class EventSignupWithConfirmView(EventSignupView):
    def get_redirect_url(self, event):
        return reverse('localevents:event_list')

@login_required
def event_list(request):
    profile = request.user.profile
    organized_events = profile.organized_events.all()
    signedup_events = Event.objects.filter(eventsignup__user_registrant=profile)

    all_events = Event.objects.exclude(
        id__in=organized_events.values_list('id', flat=True)
    ).exclude(
        id__in=signedup_events.values_list('id', flat=True)
    )

    return render(request, 'localevents/event_list.html', {
        'organized_events': organized_events,
        'signedup_events': signedup_events,
        'all_events': all_events,
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_organizer = False

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            is_organizer = event.organizer.filter(pk=profile.pk).exists()
        except Exception:
            pass

    context = {
        'event': event,
        'is_organizer': is_organizer,
        'signup_count': event.signup_count,
    }
    return render(request, 'localevents/event_detail.html', context)

@login_required
def event_create(request):
    profile = request.user.profile
    if getattr(profile, 'role', None) != 'Event Organizer':
        return redirect('localevents:event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            event.organizer.add(profile)
            return redirect(reverse('localevents:event_detail', kwargs={'pk': event.pk}))
    else:
        form = EventForm()

    return render(request, 'localevents/event_form.html', {'form': form, 'action': 'Create'})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    try:
        profile = request.user.profile
    except Exception:
        return redirect('localevents:event_list')

    if getattr(profile, 'role', None) != 'Event Organizer':
        return redirect('localevents:event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)
            if updated_event.signup_count >= updated_event.event_capacity:
                updated_event.status = Event.STATUS_FULL
            else:
                updated_event.status = Event.STATUS_AVAILABLE
            updated_event.save()
            form.save_m2m()
            return redirect(
                reverse('localevents:event_detail', kwargs={'pk': event.pk})
            )
    else:
        form = EventForm(instance=event)

    return render(request, 'localevents/event_form.html', {
        'form': form,
        'action': 'Update',
        'event': event,
    })