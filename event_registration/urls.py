from django.urls import path
from . import views


urlpatterns = [
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('registrations/', views.registration_list, name='registration_list'),
    path('registration/<int:registration_id>/', views.registration_detail, name='registration_detail'),
]