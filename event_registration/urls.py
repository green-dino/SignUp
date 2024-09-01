from django.urls import path
from . import views


urlpatterns = [
    path('', views.available_events, name='available_events'),  # URL for available events
    path('<int:event_id>/', views.register_for_event, name='register_for_event'),  # URL for registering for an event
    path('registrations/', views.registration_list, name='registration_list'),
    path('registration/<int:registration_id>/', views.registration_detail, name='registration_detail'),
    
]