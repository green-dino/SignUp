# event_registration/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Registration
from .forms import RegistrationForm
from event.models import Event

def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                registration, created = Registration.objects.select_for_update().get_or_create(
                    user=request.user,
                    event=event,
                    defaults={'status': 'pending'}
                )
                if created:
                    messages.success(request, "You have successfully registered for the event.")
                else:
                    messages.info(request, "You are already registered for this event.")
                return redirect('event_detail', event_id=event.id)
    else:
        form = RegistrationForm()
    return render(request, 'event_registration/register_event.html', {'form': form, 'event': event})

def registration_list(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'event_registration/registration_list.html', {'registrations': registrations})

def registration_detail(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    return render(request, 'event_registration/registration_detail.html', {'registration': registration})