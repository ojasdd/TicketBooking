from django.urls import path
from .views import EventListView, EventDetailView, add_to_cart, CartView
from .views import user_login,register,dashboard,home
from . import views


urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('admin/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/events/', views.manage_events, name='admin_event_list'),
    path('admin/bookings/', views.manage_bookings, name='admin_booking_list'),
    path('admin/events/manage/', views.manage_events, name='manage_events'),
    path('admin/events/add/', views.add_event, name='add_event'),
    path('admin/events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('admin/events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('admin/custom-dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('events/booked/', views.booked_events, name='booked_events'),
    path('accounts/', views.accounts, name='accounts'),
    path('admin/logout/', views.custom_logout_view, name='admin_logout'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('book/<int:pk>/', views.book_event, name='book_event'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('login/', user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('home/', home, name='home'),
]
