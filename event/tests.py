from django.test import TestCase
from django.db import models
from .models import Event, Category

class EventModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a Category instance
        category = Category.objects.create(name="Category 1")

        # Create test data
        Event.objects.create(name="Event 1", start_date="2023-01-01", end_date="2023-01-02", category=category)
        Event.objects.create(name="Event 2", start_date="2023-01-03", end_date="2023-01-04", category=category)
        Event.objects.create(name="Event 3", start_date="2023-01-02", end_date="2023-01-03", category=category)

    def test_ordering(self):
        events = Event.objects.all()
        self.assertEqual(events[0].name, "Event 1")
        self.assertEqual(events[1].name, "Event 3")
        self.assertEqual(events[2].name, "Event 2")

    def test_verbose_name(self):
        self.assertEqual(Event._meta.verbose_name, "Event")
        self.assertEqual(Event._meta.verbose_name_plural, "Events")

    def test_indexes(self):
        indexes = Event._meta.indexes
        index_fields = [index.fields for index in indexes]
        self.assertIn(['start_date'], index_fields)
        self.assertIn(['end_date'], index_fields)