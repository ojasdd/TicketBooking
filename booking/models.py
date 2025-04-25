from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200, default='Untitled Event')
    description = models.TextField(default='No description provided.')
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200, default='TBD')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    available_tickets = models.PositiveIntegerField(default=100)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    event = models.ForeignKey(Event, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)