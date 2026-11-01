from django.contrib import admin
from .models import Flight, Passenger, Booking
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_number", "airline", "source", "destination", "departure_time", "available_seats", "status")
    search_fields = ("flight_number", "airline", "source", "destination")
    list_filter = ("status", "airline")
@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone")
    search_fields = ("full_name", "email", "phone")
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_reference", "passenger", "flight", "seats_booked", "total_amount", "status")
    search_fields = ("booking_reference", "passenger__full_name", "flight__flight_number")
    list_filter = ("status",)
