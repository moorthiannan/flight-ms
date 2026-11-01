from django import forms
from .models import Flight, Passenger, Booking

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ["flight_number", "airline", "source", "destination", "departure_time",
                  "arrival_time", "total_seats", "available_seats", "fare", "status"]
        widgets = {"departure_time": DateTimeInput(), "arrival_time": DateTimeInput()}

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ["full_name", "email", "phone", "passport_number"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["passenger", "flight", "seats_booked"]
