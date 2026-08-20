"""Fixtures compartidas para las pruebas de app/reservation_service.py."""
from datetime import date

import pytest

from app.reservation_service import ReservationService
from app.repositories import InMemoryReservationRepository


@pytest.fixture
def fixed_current_date():
    """Fecha de referencia fija (lunes) usada como 'hoy' en las pruebas."""
    return date(2025, 1, 6)


@pytest.fixture
def valid_reservation_data():
    """Datos de una reserva valida, alineados con fixed_current_date."""
    return {
        "customer_name": "Ana Torres",
        "service": "asesoria",
        "duration_minutes": 30,
        "date": "2025-01-07",
        "time": "09:00",
    }


@pytest.fixture
def reservation_repository():
    """Repositorio en memoria nuevo y aislado para cada prueba."""
    return InMemoryReservationRepository()


@pytest.fixture
def reservation_service(reservation_repository):
    """Servicio de reservas con un generador de codigo de confirmacion fijo."""
    return ReservationService(
        repository=reservation_repository,
        confirmation_code_generator=lambda: "TEST-CODE-001",
    )
