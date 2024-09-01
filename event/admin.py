from django.contrib import admin
from .models import Category, Event
from event_registration.models import Registration

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'start_date', 'end_date', 'priority')
	list_filter = ('category', 'priority')
	search_fields = ('name', 'category__name', 'description', 'location', 'organizer')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'registered_at', 'updated_at')
    list_filter = ('status', 'event')
    search_fields = ('user__username', 'event__name')
