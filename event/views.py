from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Category, Event
from .forms import EventForm, CategoryForm

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
    return redirect(reverse_lazy('category_list'))

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect(reverse_lazy('category_list'))
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})

def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect(reverse_lazy('category_list'))
    else:
        form = EventForm(instance=event)
    return render(request, 'event/update_event.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'event/category_list.html', {'categories': categories})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect(reverse_lazy('category_list'))
    else:
        form = CategoryForm()
    return render(request, 'event/create_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if category.event_set.exists():
        messages.error(request, "You cannot delete this category as it contains events.")
    else:
        category.delete()
        messages.success(request, "Category deleted successfully.")
    return redirect(reverse_lazy('category_list'))

def category_events(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    events = category.events.all()
    return render(request, 'event/category_events.html', {'category': category, 'events': events})

def event_chart(request):
    categories = Category.objects.all()
    pending_counts = {
        category.name: Event.objects.filter(category=category, start_date__gt=timezone.now()).count()
        for category in categories
    }
    return render(request, 'event/event_chart.html', {'pending_counts': pending_counts})