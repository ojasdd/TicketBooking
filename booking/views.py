from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Event
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Booking
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.contrib.auth import logout
from django.shortcuts import redirect
# In booking/views.py
from django.shortcuts import render
from .models import Event, Booking
# In booking/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Booking
# In booking/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Event, Booking

def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= event.available_tickets:
            Booking.objects.create(user=request.user, event=event, quantity=quantity)
            event.available_tickets -= quantity
            event.save()
            messages.success(request, f"Successfully booked {quantity} ticket(s) for {event.title}.")
        else:
            messages.error(request, "Not enough tickets available.")
    return redirect('event_detail', pk=pk)


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


# Accounts View (User Profile/Dashboard)
def accounts(request):
    user = request.user  # Get the current logged-in user
    bookings = Booking.objects.filter(user=user)  # Get the user's bookings
    
    # You can add more user-related data here as needed
    
    return render(request, 'booking/accounts.html', {'user': user, 'bookings': bookings})


# Booked Events View
def booked_events(request):
    # Assuming there's a 'Booking' model that stores event bookings for users
    bookings = Booking.objects.filter(user=request.user)  # Filter bookings for the current logged-in user
    
    # Get the events for those bookings
    events = Event.objects.filter(id__in=[booking.event.id for booking in bookings])
    
    return render(request, 'booking/booked_events.html', {'events': events})


def custom_logout_view(request):
    logout(request)
    return redirect('admin_dashboard')  # or wherever you want to send users after logout


def admin_dashboard(request):
    return render(request, 'booking/admin/dashboard.html')

def manage_events(request):
    events = Event.objects.all()
    return render(request, 'booking/admin/event_list.html', {'events': events})

def add_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']
        location = request.POST['location']
        price = request.POST['price']

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location,
            price=price
        )
        return redirect('manage_events')
    
    return render(request, 'booking/admin/event_form.html')

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.date = request.POST['date']
        event.location = request.POST['location']
        event.price = request.POST['price']
        event.save()
        return redirect('manage_events')
    
    return render(request, 'booking/admin/event_form.html', {'event': event})

def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('manage_events')

def manage_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/admin/booking_list.html', {'bookings': bookings})

def custom_admin_dashboard(request):
    events = Event.objects.all()
    return render(request, 'booking/admin_dashboard.html', {'events': events})


def home(request):
    if request.user.is_authenticated:
        return render(request, 'booking/dashboard.html')
    return render(request, 'booking/home.html')

@login_required
def dashboard(request):
    return render(request, 'booking/dashboard.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        errors = []
        if not username or len(username) < 4:
            errors.append("Username must be at least 4 characters long")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists")
        if not email or '@' not in email:
            errors.append("Please enter a valid email address")
        if not password1 or len(password1) < 8:
            errors.append("Password must be at least 8 characters long")
        if password1 != password2:
            errors.append("Passwords don't match")
        
        if not errors:
            try:
                user = User.objects.create_user(username, email, password1)
                auth_login(request, user)
                return redirect('dashboard')  # Or your preferred redirect
            except Exception as e:
                errors.append(f"Error creating user: {str(e)}")
        
        for error in errors:
            messages.error(request, error)
    
    return render(request, 'booking/register.html')

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Please provide both username and password")
            return render(request, 'booking/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get('next', 'home')  # Default to 'home' instead of empty
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
    
    # Handle GET request
    next_url = request.GET.get('next', 'home')  # Default to 'home'
    return render(request, 'booking/login.html', {'next': next_url})

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
