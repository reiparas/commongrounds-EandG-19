from django.contrib import admin
from .models import EventType, Event


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'start_time', 'end_time', 'created_on']
    list_filter = ['category']
    search_fields = ['title', 'location']
