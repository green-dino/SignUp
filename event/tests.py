from django.test import TestCase, Client
from django.urls import reverse
from .models import Event, Category

class EventTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.event_data = {
            'name': 'Test Event',
            'category': self.category.id,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'priority': 'High',
            'description': 'This is a test event.'
        }
        self.event = Event.objects.create(**self.event_data)

    def test_create_event(self):
        response = self.client.post(reverse('create_event'), self.event_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Event.objects.count(), 2)  # One event already created in setUp

    def test_delete_event(self):
        response = self.client.post(reverse('delete_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertEqual(Event.objects.count(), 0)  # Event should be deleted

    def test_create_event_view_get(self):
        response = self.client.get(reverse('create_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/create_event.html')