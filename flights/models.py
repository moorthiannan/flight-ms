import uuid
from django.db import models
from django.utils import timezone

class Flight(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"), ("Delayed", "Delayed"),
        ("Cancelled", "Cancelled"), ("Completed", "Completed"),
    ]
    flight_number = models.CharField(max_length=12, unique=True)
    airline = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField(default=100)
    available_seats = models.PositiveIntegerField(default=100)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"{self.flight_number} - {self.source} to {self.destination}"

class Passenger(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Booking(models.Model):
    STATUS_CHOICES = [("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")]
    booking_reference = models.CharField(max_length=12, unique=True, blank=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="bookings")
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT, related_name="bookings")
    seats_booked = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="Confirmed")
    booked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = "FL" + uuid.uuid4().hex[:8].upper()
        if self.flight_id:
            self.total_amount = self.flight.fare * self.seats_booked
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_reference
