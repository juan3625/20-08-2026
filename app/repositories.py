"""Repositorio en memoria para las reservas.

Sustituye temporalmente una base de datos real. Cada instancia mantiene su
propio estado interno (no se usan variables globales), de modo que cada
prueba puede recibir un repositorio nuevo y aislado.
"""
from datetime import date, time
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.reservation_service import Reservation


class InMemoryReservationRepository:
    """Almacena reservas en una lista interna en memoria."""

    def __init__(self) -> None:
        self._reservations: List["Reservation"] = []

    def exists(self, reservation_date: date, reservation_time: time) -> bool:
        """RN-08: comprueba si ya existe una reserva para la misma fecha y hora."""
        return any(
            reservation.date == reservation_date and reservation.time == reservation_time
            for reservation in self._reservations
        )

    def save(self, reservation: "Reservation") -> None:
        """Guarda una reserva en el almacenamiento interno."""
        self._reservations.append(reservation)

    def list_all(self) -> List["Reservation"]:
        """Devuelve una copia de las reservas almacenadas."""
        return list(self._reservations)