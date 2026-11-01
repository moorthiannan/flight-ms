from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import FlightForm, PassengerForm, BookingForm
from .models import Flight, Passenger, Booking

@login_required
def dashboard(request):
    return render(request, "flights/dashboard.html", {
        "flight_count": Flight.objects.count(),
        "passenger_count": Passenger.objects.count(),
        "booking_count": Booking.objects.count(),
        "confirmed_count": Booking.objects.filter(status="Confirmed").count(),
        "recent_bookings": Booking.objects.select_related("passenger", "flight").order_by("-booked_at")[:5],
    })

@login_required
def flight_list(request):
    flights = Flight.objects.all()
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    if q:
        flights = flights.filter(Q(flight_number__icontains=q) | Q(airline__icontains=q) |
                                 Q(source__icontains=q) | Q(destination__icontains=q))
    if status:
        flights = flights.filter(status=status)
    return render(request, "flights/flight_list.html", {"flights": flights, "q": q, "status": status, "flight_status_choices": Flight.STATUS_CHOICES})

@login_required
def flight_create(request):
    form = FlightForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Flight added successfully.")
        return redirect("flight_list")
    return render(request, "flights/form.html", {"form": form, "title": "Add Flight"})

@login_required
def flight_update(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    form = FlightForm(request.POST or None, instance=flight)
    if form.is_valid():
        form.save()
        messages.success(request, "Flight updated successfully.")
        return redirect("flight_list")
    return render(request, "flights/form.html", {"form": form, "title": "Update Flight"})

@login_required
def flight_delete(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == "POST":
        flight.delete()
        messages.success(request, "Flight deleted.")
        return redirect("flight_list")
    return render(request, "flights/confirm_delete.html", {"object": flight, "title": "Delete Flight"})

@login_required
def passenger_list(request):
    passengers = Passenger.objects.all().order_by("-created_at")
    q = request.GET.get("q", "")
    if q:
        passengers = passengers.filter(Q(full_name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
    return render(request, "flights/passenger_list.html", {"passengers": passengers, "q": q})

@login_required
def passenger_create(request):
    form = PassengerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Passenger added.")
        return redirect("passenger_list")
    return render(request, "flights/form.html", {"form": form, "title": "Add Passenger"})

@login_required
def passenger_update(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    form = PassengerForm(request.POST or None, instance=passenger)
    if form.is_valid():
        form.save()
        messages.success(request, "Passenger updated.")
        return redirect("passenger_list")
    return render(request, "flights/form.html", {"form": form, "title": "Update Passenger"})

@login_required
def passenger_delete(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    if request.method == "POST":
        passenger.delete()
        messages.success(request, "Passenger deleted.")
        return redirect("passenger_list")
    return render(request, "flights/confirm_delete.html", {"object": passenger, "title": "Delete Passenger"})

@login_required
def booking_list(request):
    bookings = Booking.objects.select_related("passenger", "flight").order_by("-booked_at")
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    if q:
        bookings = bookings.filter(Q(booking_reference__icontains=q) |
                                   Q(passenger__full_name__icontains=q) |
                                   Q(flight__flight_number__icontains=q))
    if status:
        bookings = bookings.filter(status=status)
    return render(request, "flights/booking_list.html", {"bookings": bookings, "q": q, "status": status})

@login_required
def booking_create(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        if booking.seats_booked < 1:
            form.add_error("seats_booked", "Book at least one seat.")
        elif booking.flight.status != "Scheduled":
            form.add_error("flight", "Only scheduled flights can be booked.")
        elif booking.seats_booked > booking.flight.available_seats:
            form.add_error("seats_booked", f"Only {booking.flight.available_seats} seats are available.")
        else:
            with transaction.atomic():
                flight = Flight.objects.select_for_update().get(pk=booking.flight_id)
                if booking.seats_booked > flight.available_seats:
                    form.add_error("seats_booked", f"Only {flight.available_seats} seats are available.")
                else:
                    flight.available_seats -= booking.seats_booked
                    flight.save(update_fields=["available_seats"])
                    booking.flight = flight
                    booking.save()
                    messages.success(request, f"Booking confirmed. Reference: {booking.booking_reference}")
                    return redirect("booking_list")
    return render(request, "flights/form.html", {"form": form, "title": "Create Booking"})

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking.objects.select_related("flight"), pk=pk)
    if request.method == "POST" and booking.status == "Confirmed":
        with transaction.atomic():
            booking.status = "Cancelled"
            booking.save(update_fields=["status"])
            booking.flight.available_seats = min(booking.flight.total_seats,
                                                  booking.flight.available_seats + booking.seats_booked)
            booking.flight.save(update_fields=["available_seats"])
        messages.success(request, "Booking cancelled and seats released.")
    return redirect("booking_list")
