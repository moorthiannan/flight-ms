# Flight Management System (Django)

## Features
- User registration, login and logout
- Dashboard with flight, booking and passenger counts
- Flight CRUD with search and status filter
- Passenger CRUD
- Booking creation, listing and cancellation
- Booking reference generation and total fare calculation
- Prevents booking more seats than the available capacity
- Django admin

## Run on Windows PowerShell
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations flights
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

The SQLite database file `db.sqlite3` is created in the same folder as
`manage.py` when `python manage.py migrate` runs. It is not necessary to
create this file manually.

This is a classroom/lab demonstration, not a production airline booking system.
