from django.urls import path, include

urlpatterns = [
    path('', include('booking.urls')),  # this makes '/' point to your app
]
