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
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from .models import Event, Booking
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login



class AdminLoginView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('admin_dashboard')
        return render(request, 'booking/admin/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not authorized as Admin.")
            return render(request, 'booking/admin/login.html')


@method_decorator(login_required, name='dispatch')
class AccountsView(View):
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking/accounts.html', {'user': request.user, 'bookings': bookings})


@method_decorator(login_required, name='dispatch')
class BookedEventsView(View):
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        events = Event.objects.filter(id__in=[booking.event.id for booking in bookings])
        return render(request, 'booking/booked_events.html', {'events': events})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        if request.user.is_staff:
            return redirect('admin_login')
        return redirect('login')


class AdminDashboardView(View):
    def get(self, request):
        return render(request, 'booking/admin/dashboard.html')


class ManageEventsView(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'booking/admin/event_list.html', {'events': events})


class AddEventView(View):
    def get(self, request):
        return render(request, 'booking/admin/event_form.html')

    def post(self, request):
        Event.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            date=request.POST['date'],
            location=request.POST['location'],
            price=request.POST['price'],
            available_tickets=request.POST['available_tickets']
        )
        return redirect('manage_events')


class EditEventView(View):
    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        return render(request, 'booking/admin/event_form.html', {'event': event})

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.date = request.POST['date']
        event.location = request.POST['location']
        event.price = request.POST['price']
        event.available_tickets = request.POST['available_tickets']
        event.save()
        return redirect('manage_events')


class DeleteEventView(View):
    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        event.delete()
        return redirect('manage_events')


class ManageBookingsView(View):
    def get(self, request):
        bookings = Booking.objects.all()
        return render(request, 'booking/admin/booking_list.html', {'bookings': bookings})


class CustomAdminDashboardView(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'booking/admin_dashboard.html', {'events': events})


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'booking/dashboard.html')
        return render(request, 'booking/home.html')


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        return render(request, 'booking/dashboard.html')


@method_decorator(csrf_protect, name='dispatch')
class RegisterView(View):
    def get(self, request):
        return render(request, 'booking/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
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
                return redirect('/')
            except Exception as e:
                errors.append(f"Error creating user: {str(e)}")
        for error in errors:
            messages.error(request, error)
        return render(request, 'booking/register.html')


@method_decorator(csrf_protect, name='dispatch')
class UserLoginView(View):
    def get(self, request):
        next_url = request.GET.get('next', '/')
        return render(request, 'booking/login.html', {'next': next_url})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, "Please provide both username and password")
            return render(request, 'booking/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'booking/login.html')

class EventListView(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'booking/event_list.html', {'events': events})

class EventDetailView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'booking/event_detail.html', {'event': event})


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
