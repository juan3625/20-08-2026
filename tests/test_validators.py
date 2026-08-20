from datetime import date, time, timedelta  

import pytest

from app.exceptions import InvalidCustomerError, InvalidDurationError, InvalidReservationDateError, InvalidReservationTimeError
from app.validators import validate_customer_name, validate_duration, validate_service, validate_reservation_date, validate_reservation_time

def test_validate_customer_name_removes_whitespace_and_validates_length():
    result = validate_customer_name("  John Doe  ")
    assert result == "John Doe"


def test_validate_customer_name_rejects_short_names():
    with pytest.raises(InvalidCustomerError, match="Customer name must be at least 3 characters long."):
        validate_customer_name("Jo")



@pytest.mark.parametrize(
    "duration",
    [30, 60, 90]
)

def test_validate_duration(duration):
    assert validate_duration(duration) == duration

@pytest.mark.parametrize(
    "invalid_duration",
    [15, 45, 120]
)
def test_validate_duration_rejects_invalid_durations(invalid_duration):
    with pytest.raises(InvalidDurationError):
        validate_duration(invalid_duration)


@pytest.mark.parametrize(
    "expected_service, service",
    [("ASESORIA", "asesoria"), ("SOPORTE", "soporte"), ("DESARROLLO", "desarrollo")],
)
def test_validate_service(expected_service, service):
    assert validate_service(service) == expected_service


#parametrizacion con id para los valores permitidos de duracion

@pytest.mark.parametrize(
    "duration",
    [pytest.param(30, id="media-hora"), pytest.param(60, id="una-hora"), pytest.param(90, id="hora-y-media")],
)

def test_validate_duration_accepts_allowed_values_with_id(duration):
    assert validate_duration(duration) == duration

#fixture para el nombre del cliente

@pytest.fixture
def  customer_name():
    return { "name": "  Alice Smith  ",
             "service": "asesoria", 
             "duration": 60,}

def test_validate_customer_name_fixture(customer_name):
    result = validate_customer_name(customer_name["name"])
    assert result == "Alice Smith"


def test_validate_reservation_date_accepts_future_weekday():
    today = date.today()
    future_weekday = today + timedelta(days=(7 - today.weekday()))
    assert validate_reservation_date(future_weekday) == future_weekday


def test_validate_reservation_date_rejects_past_date():
    past_date = date(2020, 1, 1)
    with pytest.raises(InvalidReservationDateError):
        validate_reservation_date(past_date)

@pytest.mark.parametrize(
    "weekend_date",
    [
        pytest.param(date(2026, 8, 1), id="Saturday"),  # A Saturday
        pytest.param(date(2026, 8, 2), id="Sunday"),    # A Sunday
    ],
)
def test_validate_reservation_date_rejects_weekend_dates(weekend_date):
    with pytest.raises(InvalidReservationDateError):
        validate_reservation_date(weekend_date)

@pytest.mark.parametrize(
    "reservation_time, duration",
    [
        pytest.param(time(9, 0), 30, id="apertura"),
        pytest.param(time(12, 30), 60, id="mediodia"),
        pytest.param(time(16, 30), 30, id="ultimo-bloque"),
        pytest.param(time(16, 0), 60, id="ultima-hora"),
    ],
)


def test_validate_reservation_time(reservation_time, duration):
    assert validate_reservation_time(reservation_time, duration) == reservation_time

@pytest.mark.parametrize(
    "reservation_time, duration",
    [
        pytest.param(time(7, 59), 30, id="antes-apertura"),
        pytest.param(time(16, 30), 60, id="finaliza-despues-cierre"),
        pytest.param(time(18, 0), 30, id="inicia-en-cierre"),
    ],
)
def test_validate_reservation_time_rejects_invalid_times(reservation_time, duration):
    with pytest.raises(InvalidReservationTimeError):
        validate_reservation_time(reservation_time, duration)