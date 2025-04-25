from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Event

class EventListView(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'booking/event_list.html', {'events': events})

class EventDetailView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'booking/event_detail.html', {'event': event})

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        items = []
        total = 0
        for pk, quantity in cart.items():
            event = get_object_or_404(Event, pk=pk)
            subtotal = event.price * quantity
            items.append({'event': event, 'quantity': quantity, 'subtotal': subtotal})
            total += subtotal
        return render(request, 'booking/cart.html', {'items': items, 'total': total})
