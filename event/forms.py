from django import forms
from django.core.exceptions import ValidationError
from .models import Event, Category

class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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
        error_messages = {
            'name': {
                'required': 'Event name is required.',
                'max_length': 'Event name is too long.',
            },
            'start_date': {
                'required': 'Start date and time are required.',
            },
            'end_date': {
                'required': 'End date and time are required.',
            },
        }

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date should be after start date")
        return end_date

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')
        if priority is not None and (priority < 1 or priority > 5):
            raise ValidationError("Priority must be between 1 and 5")
        return priority

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and Event.objects.filter(name=name).exists():
            raise ValidationError('An event with this name already exists.')
        return name

    def clean(self):
        cleaned_data = super().clean()
        # Additional cross-field validation can be added here if needed
        return cleaned_data

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
        error_messages = {
            'name': {
                'required': 'Category name is required.',
                'max_length': 'Category name is too long.',
                'unique': 'A category with this name already exists.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and Category.objects.filter(name=name).exists():
            raise ValidationError("A category with this name already exists.")
        return name