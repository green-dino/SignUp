# services.py
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from .models import Category, Event

class CategoryService:
    @staticmethod
    def event_count(category):
        return category.events.count()

    @staticmethod
    def latest_event(category):
        return category.events.order_by('-start_date').first()

    @staticmethod
    def total_event_duration(category):
        return category.events.aggregate(
            total_duration=Sum(ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField()))
        )['total_duration']

    @staticmethod
    def upcoming_events_count(category):
        return category.events.filter(start_date__gt=timezone.now()).count()

    @staticmethod
    def ongoing_events_count(category):
        now = timezone.now()
        return category.events.filter(start_date__lte=now, end_date__gte=now).count()

    @staticmethod
    def past_events_count(category):
        return category.events.filter(end_date__lt=timezone.now()).count()

class EventService:
    @staticmethod
    def is_past_event(event):
        return event.end_date < timezone.now()

    @staticmethod
    def is_upcoming_event(event):
        return event.start_date > timezone.now()

    @staticmethod
    def is_ongoing_event(event):
        now = timezone.now()
        return event.start_date <= now <= event.end_date

    @staticmethod
    def event_duration(event):
        return event.end_date - event.start_date

    @staticmethod
    def formatted_start_date(event):
        return event.start_date.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def formatted_end_date(event):
        return event.end_date.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def priority_label(event):
        return dict(Event.PRIORITY_CHOICES).get(event.priority, 'Unknown')

    @staticmethod
    def event_summary(event):
        return f"{event.name} ({EventService.priority_label(event)}) - {EventService.formatted_start_date(event)} to {EventService.formatted_end_date(event)}"