from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")

    def __str__(self):
        return self.name

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

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date should be after start date")

    class Meta:
        ordering = ['start_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]