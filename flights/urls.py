from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("flights/", views.flight_list, name="flight_list"),
    path("flights/add/", views.flight_create, name="flight_create"),
    path("flights/<int:pk>/edit/", views.flight_update, name="flight_update"),
    path("flights/<int:pk>/delete/", views.flight_delete, name="flight_delete"),
    path("passengers/", views.passenger_list, name="passenger_list"),
    path("passengers/add/", views.passenger_create, name="passenger_create"),
    path("passengers/<int:pk>/edit/", views.passenger_update, name="passenger_update"),
    path("passengers/<int:pk>/delete/", views.passenger_delete, name="passenger_delete"),
    path("bookings/", views.booking_list, name="booking_list"),
    path("bookings/add/", views.booking_create, name="booking_create"),
    path("bookings/<int:pk>/cancel/", views.booking_cancel, name="booking_cancel"),
]
