from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Category, Event
from .forms import EventForm, CategoryForm
from django.core.paginator import Paginator

def handle_form_submission(request, form, success_message, redirect_url):
    if form.is_valid():
        form.save()
        messages.success(request, success_message)
        return redirect(redirect_url)
    messages.error(request, "There was an error with your submission.")
    return None

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
    return redirect(reverse_lazy('category_list'))

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        response = handle_form_submission(request, form, "Event created successfully.", reverse_lazy('category_list'))
        if response:
            return response
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})

def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        response = handle_form_submission(request, form, "Event updated successfully.", reverse_lazy('category_list'))
        if response:
            return response
    else:
        form = EventForm(instance=event)
    return render(request, 'event/update_event.html', {'form': form})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event/event_detail.html', {'event': event})

def category_list(request):
    categories = Category.objects.all().prefetch_related('events')
    return render(request, 'event/category_list.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        response = handle_form_submission(request, form, "Category created successfully.", reverse_lazy('category_list'))
        if response:
            return response
    else:
        form = CategoryForm()
    return render(request, 'event/create_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if category.events.exists():
        messages.error(request, "You cannot delete this category as it contains events.")
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")
    return redirect(reverse_lazy('category_list'))

def category_events(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    events = category.events.all()
    for event in events:
        event.duration = event.event_duration()
        event.status = 'Pending' if event.is_upcoming_event() else 'Completed' if event.is_past_event() else 'Ongoing'
    return render(request, 'event/category_events.html', {'category': category, 'events': events})

def event_chart(request):
    categories = Category.objects.all().prefetch_related('events')
    
    pending_counts = {
        category: category.upcoming_events_count()
        for category in categories
    }
    
    event_durations = {
        category: category.total_event_duration()
        for category in categories
    }
    
    total_events = {
        category: category.events.count()
        for category in categories
    }
    
    average_duration = {
        category: (category.total_event_duration().total_seconds() / category.events.count() / 3600) if category.events.count() > 0 else 0
        for category in categories
    }
    
    max_duration = max(average_duration.values(), default=0)

    paginator = Paginator(list(average_duration.items()), 10)  # Show 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'event/event_chart.html', {
        'pending_counts': pending_counts,
        'event_durations': event_durations,
        'total_events': total_events,
        'average_duration': dict(page_obj.object_list),
        'max_duration': max_duration,
        'page_obj': page_obj,
    })