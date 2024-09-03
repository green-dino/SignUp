from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Registration, get_available_events
from .forms import RegistrationForm
from event.models import Event


def available_events(request):
    events = get_available_events()
    return render(request, 'event_registration/available_events.html', {'events': events})

def register_for_event(request, event_id):
#    if not request.user.is_authenticated:
#        messages.error(request, "You need to be logged in to register for an event.")
#        return redirect('login')

    event = get_object_or_404(Event, id=event_id)
    if event.start_date < timezone.now():
        messages.error(request, "Cannot register for past events.")
        return redirect('available_events')

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
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your registrations.")
        return redirect('login')

    registrations = Registration.objects.filter(user=request.user).select_related('event')
    return render(request, 'event_registration/registration_list.html', {'registrations': registrations})

def registration_detail(request, registration_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view registration details.")
        return redirect('login')

    registration = get_object_or_404(Registration.objects.select_related('event'), id=registration_id)
    return render(request, 'event_registration/registration_detail.html', {'registration': registration})