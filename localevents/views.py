from django.shortcuts import render, get_object_or_404
from .models import Event


def event_list(request):
    events = Event.objects.all()
    return render(request, 'localevents/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'localevents/event_detail.html', {'event': event})
