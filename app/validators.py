from datetime import datetime, time, date, timedelta
from app.exceptions import (
    InvalidCustomerError,
    InvalidServiceError,
    InvalidDurationError,
    InvalidReservationDateError,
    InvalidReservationTimeError,
)

ALLOWED_SERVICES = ["ASESORIA", "SOPORTE", "DEMOSTRACION", "DESARROLLO"]
ALLOWED_DURATIONS = [30, 60, 90]

OPENING_TIME = time(8, 0)
CLOSING_TIME = time(17, 0)


def validate_customer_name(customer_name: str) -> str:
    normalized_name = customer_name.strip()
    if len(normalized_name) < 3:
        raise InvalidCustomerError("Customer name must be at least 3 characters long.")
    return normalized_name


def validate_service(service: str) -> str:
    normalized_service = service.strip().upper()
    if normalized_service not in ALLOWED_SERVICES:
        raise InvalidServiceError(f"Service must be one of {ALLOWED_SERVICES}.")
    return normalized_service


def validate_duration(duration: int) -> int:
    if duration not in ALLOWED_DURATIONS:
        raise InvalidDurationError(f"Duration must be one of {ALLOWED_DURATIONS}.")
    return duration


def validate_reservation_date(reservation_date: date) -> date:
    today = date.today()
    if reservation_date < today:
        raise InvalidReservationDateError("Reservation date cannot be in the past.")
    if reservation_date.weekday() >= 5:
        raise InvalidReservationDateError("Reservations are only allowed on weekdays.")
    return reservation_date


