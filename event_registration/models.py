from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='pending')
    ticket_number = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"

    def __str__(self):
        return f"User: {self.user.username}, Event: {self.event.name}"

    @property
    def is_paid(self):
        return self.payment_status == 'paid'

    @property
    def is_pending(self):
        return self.payment_status == 'pending'
