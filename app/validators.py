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


def validate_reservation_time(reservation_time: time, duration: int = 30) -> time:
    if reservation_time < OPENING_TIME:
        raise InvalidReservationTimeError("La reserva no puede ser antes de la hora de apertura.")

    dummy_date = datetime(2000, 1, 1)
    start_dt = datetime.combine(dummy_date, reservation_time)
    end_dt = start_dt + timedelta(minutes=duration)
    closing_dt = datetime.combine(dummy_date, CLOSING_TIME)

    if end_dt > closing_dt:
        raise InvalidReservationTimeError("La reserva finaliza después del horario de cierre.")

    if reservation_time >= CLOSING_TIME:
        raise InvalidReservationTimeError("La reserva no puede iniciar en o después del horario de cierre.")

    return reservation_time