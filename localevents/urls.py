from django.urls import path

from . import views

app_name = 'localevents'

urlpatterns = [
    path('events', views.event_list, name='event_list'),
    path('event/add', views.event_create, name='event_create'),
    path('event/<int:pk>', views.event_detail, name='event_detail'),
    path('event/<int:pk>/edit', views.event_update, name='event_update'),
    path(
        'event/<int:pk>/signup',
        views.EventSignupView.as_view(),
        name='event_signup',
    ),
    path(
        'event/<int:pk>/signup/guest',
        views.EventSignupFormView.as_view(),
        name='event_signup_guest',
    ),
]
