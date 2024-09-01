from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Registration, get_available_events
from .forms import RegistrationForm
from event.models import Event

def available_events(request):
    events = get_available_events()
    return render(request, 'event_registration/available_events.html', {'events': events})

@login_required
def register_for_event(request, event_id):
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

@login_required
def registration_list(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    return render(request, 'event_registration/registration_list.html', {'registrations': registrations})

@login_required
def registration_detail(request, registration_id):
    registration = get_object_or_404(Registration.objects.select_related('event'), id=registration_id)
    return render(request, 'event_registration/registration_detail.html', {'registration': registration})