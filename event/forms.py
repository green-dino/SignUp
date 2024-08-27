from django import forms
from .models import Event, Category
from django.core.exceptions import ValidationError

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'category', 'start_date', 'end_date', 
            'priority', 'description', 'location', 'organizer'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Event Name',
            'category': 'Category',
            'start_date': 'Start Date and Time',
            'end_date': 'End Date and Time',
            'priority': 'Priority Level',
            'description': 'Event Description',
            'location': 'Event Location',
            'organizer': 'Event Organizer',
        }
        help_texts = {
            'start_date': 'Enter the start date and time of the event.',
            'end_date': 'Enter the end date and time of the event.',
        }

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date should be after start date")
        return end_date

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Category Name',
        }
        help_texts = {
            'name': 'Enter a unique name for the category.',
        }