from django.urls import path
from .views import EventListView, EventDetailView, add_to_cart, CartView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
]
