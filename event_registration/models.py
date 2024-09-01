from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from event.models import Event

class RegistrationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('event', 'user')

    def confirmed(self):
        return self.get_queryset().filter(status='confirmed')

    def cancelled(self):
        return self.get_queryset().filter(status='cancelled')

    def pending(self):
        return self.get_queryset().filter(status='pending')

class Registration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
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
        if self.event.start_date < timezone.now():
            raise ValidationError("Cannot register for past events")

    def is_confirmed(self):
        return self.status == 'confirmed'

    def is_cancelled(self):
        return self.status == 'cancelled'

    def is_pending(self):
        return self.status == 'pending'

# Adding a method to fetch available events for registration
def get_available_events():
    return Event.objects.filter(start_date__gte=timezone.now())