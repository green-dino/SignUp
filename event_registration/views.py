from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .models import Registration

@login_required
def register_for_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    
    if event.is_past_event():
        messages.error(request, "This event has already passed.")
        return redirect('event_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()
            messages.success(request, "You have successfully registered for the event!")
            return redirect('event_detail', pk=event_id)
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form, 'event': event})
