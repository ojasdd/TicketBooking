from django.urls import path
from .views import EventListView, EventDetailView, CartView
# from .views import user_login,register,dashboard,home
from . import views
from django.urls import path
from .views import (
    EventListView, EventDetailView, CartView,
    AdminLoginView, AdminDashboardView, ManageEventsView, AddEventView,
    EditEventView, DeleteEventView, ManageBookingsView, CustomAdminDashboardView,
    BookedEventsView, AccountsView,  LogoutView, DashboardView,
    RegisterView, UserLoginView
)


urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('admin/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/events/', ManageEventsView.as_view(), name='manage_events'),
    path('admin/bookings/', ManageBookingsView.as_view(), name='admin_booking_list'),
    path('admin/events/add/', AddEventView.as_view(), name='add_event'),
    path('admin/events/edit/<int:event_id>/', EditEventView.as_view(), name='edit_event'),
    path('admin/events/delete/<int:event_id>/', DeleteEventView.as_view(), name='delete_event'),
    path('admin/custom-dashboard/', CustomAdminDashboardView.as_view(), name='custom_admin_dashboard'),
    path('events/booked/', BookedEventsView.as_view(), name='booked_events'),
    path('accounts/', AccountsView.as_view(), name='accounts'),
    # path('admin/logout/', AdminLogoutView.as_view(), name='admin_logout'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    # path('book/<int:pk>/', BookEventView.as_view(), name='book_event'),
    # path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
