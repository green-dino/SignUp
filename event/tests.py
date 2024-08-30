import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event, Category

@pytest.mark.django_db
def test_create_event(client):
    category = Category.objects.create(name="Test Category")
    url = reverse('create_event')
    data = {
        'name': 'Test Event',
        'category': category.id,
        'start_date': '2023-12-01T10:00',
        'end_date': '2023-12-01T12:00',
        'priority': 3,
        'description': 'This is a test event.',
        'location': 'Test Location',
        'organizer': 'Test Organizer'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after successful creation
    assert Event.objects.filter(name='Test Event').exists()

@pytest.mark.django_db
def test_update_event(client):
    category = Category.objects.create(name="Test Category")
    event = Event.objects.create(
        name='Test Event',
        category=category,
        start_date='2023-12-01T10:00',
        end_date='2023-12-01T12:00',
        priority=3,
        description='This is a test event.',
        location='Test Location',
        organizer='Test Organizer'
    )
    url = reverse('update_event', args=[event.id])
    data = {
        'name': 'Updated Test Event',
        'category': category.id,
        'start_date': '2023-12-01T10:00',
        'end_date': '2023-12-01T12:00',
        'priority': 3,
        'description': 'This is an updated test event.',
        'location': 'Updated Test Location',
        'organizer': 'Updated Test Organizer'
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after successful update
    event.refresh_from_db()
    assert event.name == 'Updated Test Event'

@pytest.mark.django_db
def test_delete_event(client):
    category = Category.objects.create(name="Test Category")
    event = Event.objects.create(
        name='Test Event',
        category=category,
        start_date='2023-12-01T10:00',
        end_date='2023-12-01T12:00',
        priority=3,
        description='This is a test event.',
        location='Test Location',
        organizer='Test Organizer'
    )
    url = reverse('delete_event', args=[event.id])
    response = client.post(url)
    assert response.status_code == 302  # Redirect after successful deletion
    assert not Event.objects.filter(id=event.id).exists()