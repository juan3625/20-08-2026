"""Pruebas unitarias para app/reservation_service.py.

Se prueba la logica coordinada del servicio (validaciones + repositorio +
generador de codigo) sin FastAPI, sin Uvicorn y sin base de datos real.
"""
from datetime import date, time

import pytest

from app.exceptions import (
    DuplicateReservationError,
    InvalidCustomerNameError,
    InvalidDurationError,
    InvalidReservationDateError,
    InvalidReservationTimeError,
    InvalidServiceError,
)
from app.reservation_service import ReservationService
from app.repositories import InMemoryReservationRepository


# ---------------------------------------------------------------------------
# Creacion exitosa de una reserva
# ---------------------------------------------------------------------------


def test_valid_reservation_is_created_with_confirmed_status(
    reservation_service, valid_reservation_data, fixed_current_date
):
    # Act
    reservation = reservation_service.create(valid_reservation_data, fixed_current_date)
    # Assert
    assert reservation.status == "confirmed"


def test_confirmation_code_comes_from_injected_dependency(
    reservation_repository, valid_reservation_data, fixed_current_date
):
    # Arrange: generador de codigo controlado directamente en la prueba
    service = ReservationService(
        repository=reservation_repository,
        confirmation_code_generator=lambda: "FIXED-CODE-001",
    )
    # Act
    reservation = service.create(valid_reservation_data, fixed_current_date)
    # Assert
    assert reservation.confirmation_code == "FIXED-CODE-001"


def test_customer_name_and_service_are_normalized_in_created_reservation(
    reservation_service, fixed_current_date
):
    # Arrange
    data = {
        "customer_name": "  Carlos Ruiz  ",
        "service": "SOPORTE",
        "duration_minutes": 60,
        "date": "2025-01-08",
        "time": "10:00",
    }
    # Act
    reservation = reservation_service.create(data, fixed_current_date)
    # Assert
    assert reservation.customer_name == "Carlos Ruiz"
    assert reservation.service == "soporte"


def test_valid_reservation_is_stored_in_repository(
    reservation_service, reservation_repository, valid_reservation_data, fixed_current_date
):
    # Act
    reservation_service.create(valid_reservation_data, fixed_current_date)
    # Assert
    stored_reservations = reservation_repository.list_all()
    assert len(stored_reservations) == 1
    assert stored_reservations[0].status == "confirmed"


def test_reservation_dataclass_fields_match_input(
    reservation_service, valid_reservation_data, fixed_current_date
):
    # Act
    reservation = reservation_service.create(valid_reservation_data, fixed_current_date)
    # Assert
    assert reservation.date == date(2025, 1, 7)
    assert reservation.time == time(9, 0)
    assert reservation.duration_minutes == 30


# ---------------------------------------------------------------------------
# Reserva duplicada (RN-08)
# ---------------------------------------------------------------------------


def test_duplicate_reservation_raises_error(
    reservation_service, valid_reservation_data, fixed_current_date
):
    # Arrange: se crea una primera reserva valida
    reservation_service.create(valid_reservation_data, fixed_current_date)
    # Act / Assert: la misma fecha y hora deben producir DuplicateReservationError
    with pytest.raises(DuplicateReservationError):
        reservation_service.create(valid_reservation_data, fixed_current_date)


def test_same_time_different_date_is_not_considered_duplicate(
    reservation_service, valid_reservation_data, fixed_current_date
):
    # Arrange
    reservation_service.create(valid_reservation_data, fixed_current_date)
    other_day_data = dict(valid_reservation_data, date="2025-01-08")
    # Act
    reservation = reservation_service.create(other_day_data, fixed_current_date)
    # Assert
    assert reservation.status == "confirmed"


# ---------------------------------------------------------------------------
# No persistencia ante error de validacion
# ---------------------------------------------------------------------------


def test_invalid_data_does_not_persist_any_reservation(
    reservation_service, reservation_repository, valid_reservation_data, fixed_current_date
):
    # Arrange: nombre invalido (menos de 3 caracteres)
    invalid_data = dict(valid_reservation_data, customer_name="Al")
    # Act
    with pytest.raises(InvalidCustomerNameError):
        reservation_service.create(invalid_data, fixed_current_date)
    # Assert
    assert reservation_repository.list_all() == []


# ---------------------------------------------------------------------------
# Validaciones invalidas parametrizadas (varias reglas a la vez)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "overrides, expected_exception",
    [
        ({"customer_name": "Al"}, InvalidCustomerNameError),
        ({"service": "consultoria"}, InvalidServiceError),
        ({"duration_minutes": 45}, InvalidDurationError),
        ({"date": "2025-01-01"}, InvalidReservationDateError),  # fecha pasada
        ({"date": "2025-01-11"}, InvalidReservationDateError),  # sabado
        ({"time": "07:30"}, InvalidReservationTimeError),
    ],
)
def test_create_with_invalid_field_raises_expected_exception(
    reservation_service, valid_reservation_data, fixed_current_date, overrides, expected_exception
):
    # Arrange
    data = dict(valid_reservation_data, **overrides)
    # Act / Assert
    with pytest.raises(expected_exception):
        reservation_service.create(data, fixed_current_date)


# ---------------------------------------------------------------------------
# Independencia entre pruebas
# ---------------------------------------------------------------------------


def test_new_repository_instance_starts_empty():
    # Arrange / Act
    repository = InMemoryReservationRepository()
    # Assert
    assert repository.list_all() == []


def test_repository_fixture_is_isolated_between_tests(reservation_repository):
    # Este test corre en cualquier orden respecto a los demas: si otra
    # prueba hubiera "filtrado" estado global, este repositorio no lo veria.
    assert reservation_repository.list_all() == []