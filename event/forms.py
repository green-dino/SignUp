from django import forms
from .models import Event, Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'category', 'start_date', 'end_date', 'priority', 'description', 'location', 'organizer']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']