from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, DurationField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})

    def event_count(self):
        return self.events.count()

    def latest_event(self):
        return self.events.order_by('-start_date').first()

    def total_event_duration(self):
        return self.events.aggregate(
            total_duration=Sum(ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField()))
        )['total_duration']

    def upcoming_events_count(self):
        return self.events.filter(start_date__gt=timezone.now()).count()

    def ongoing_events_count(self):
        now = timezone.now()
        return self.events.filter(start_date__lte=now, end_date__gte=now).count()

    def past_events_count(self):
        return self.events.filter(end_date__lt=timezone.now()).count()

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

class Event(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    name = models.CharField(max_length=100, verbose_name="Event Name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1, verbose_name="Priority")
    description = models.TextField(default='', blank=True, verbose_name="Description")
    location = models.CharField(max_length=255, default='', blank=True, verbose_name="Location")
    organizer = models.CharField(max_length=100, default='', blank=True, verbose_name="Organizer")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date should be after start date")
        if self.start_date < timezone.now():
            raise ValidationError("Start date should be in the future")

    def is_past_event(self):
        return self.end_date < timezone.now()

    def is_upcoming_event(self):
        return self.start_date > timezone.now()

    def is_ongoing_event(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def event_duration(self):
        return self.end_date - self.start_date

    def formatted_start_date(self):
        return self.start_date.strftime('%Y-%m-%d %H:%M:%S')

    def formatted_end_date(self):
        return self.end_date.strftime('%Y-%m-%d %H:%M:%S')

    def priority_label(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority, 'Unknown')

    def event_summary(self):
        return f"{self.name} ({self.priority_label()}) - {self.formatted_start_date()} to {self.formatted_end_date()}"

    class Meta:
        ordering = ['start_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]