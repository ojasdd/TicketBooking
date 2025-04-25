from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'price')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description')
    ordering = ('-date',)
