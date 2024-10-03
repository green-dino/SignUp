from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from event.models import Event

class RegistrationManager(models.Manager):
    """
    Custom manager for Registration model to add additional query methods.
    """
    def get_queryset(self):
        return super().get_queryset().select_related('event', 'user')

    def confirmed(self):
        return self.get_queryset().filter(status=Registration.Status.CONFIRMED)

    def cancelled(self):
        return self.get_queryset().filter(status=Registration.Status.CANCELLED)

    def pending(self):
        return self.get_queryset().filter(status=Registration.Status.PENDING)

class Registration(models.Model):
    """
    Model representing a registration for an event by a user.
    """
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RegistrationManager()

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-registered_at']
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

    def clean(self):
        """
        Custom validation to ensure the event is not in the past.
        """
        if self.event.start_date < timezone.now():
            raise ValidationError("Cannot register for past events")

    def is_confirmed(self):
        return self.status == self.Status.CONFIRMED

    def is_cancelled(self):
        return self.status == self.Status.CANCELLED

    def is_pending(self):
        return self.status == self.Status.PENDING

def get_available_events():
    """
    Fetch events that are starting in the future.
    """
    return Event.objects.filter(start_date__gte=timezone.now())