"""Servicio de aplicacion que coordina las reglas de negocio de reservas."""
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, Callable, Dict

from app.exceptions import DuplicateReservationError
from app.repositories import InMemoryReservationRepository
from app.validators import (
    validate_customer_name,
    validate_duration,
    validate_reservation_date,
    validate_reservation_time,
    validate_service,
)


@dataclass
class Reservation:
    """Representa una reserva ya validada y confirmada."""

    customer_name: str
    service: str
    duration_minutes: int
    date: date
    time: time
    status: str
    confirmation_code: str


class ReservationService:
    """Aplica las reglas de negocio y coordina el repositorio y el generador de codigos.

    Las dependencias (repositorio y generador de codigo de confirmacion) se
    reciben por constructor para que puedan sustituirse por dobles de prueba
    controlables (RN-10).
    """

    def __init__(
        self,
        repository: InMemoryReservationRepository,
        confirmation_code_generator: Callable[[], str],
    ) -> None:
        self._repository = repository
        self._generate_confirmation_code = confirmation_code_generator

    def create(self, data: Dict[str, Any], current_date: date) -> Reservation:
        """Valida los datos recibidos y, si son correctos, crea y guarda la reserva.

        El orden de validacion sigue la numeracion de las reglas de negocio.
        Si cualquier validacion falla, se lanza la excepcion correspondiente
        y no se guarda ninguna reserva.
        """
        customer_name = validate_customer_name(data.get("customer_name"))
        service = validate_service(data.get("service")).lower()
        duration_minutes = validate_duration(data.get("duration_minutes"))

        raw_date = data.get("date")
        parsed_date = (
            raw_date if isinstance(raw_date, date) else datetime.strptime(raw_date, "%Y-%m-%d").date()
        )
        reservation_date = validate_reservation_date(parsed_date, current_date)

        raw_time = data.get("time")
        parsed_time = (
            raw_time if isinstance(raw_time, time) else datetime.strptime(raw_time, "%H:%M").time()
        )
        reservation_time = validate_reservation_time(parsed_time, duration_minutes)

        # RN-08: no pueden existir dos reservas para la misma fecha y hora.
        if self._repository.exists(reservation_date, reservation_time):
            raise DuplicateReservationError(
                f"Ya existe una reserva para {reservation_date} a las {reservation_time}."
            )

        reservation = Reservation(
            customer_name=customer_name,
            service=service,
            duration_minutes=duration_minutes,
            date=reservation_date,
            time=reservation_time,
            status="confirmed",  # RN-09
            confirmation_code=self._generate_confirmation_code(),  # RN-10
        )
        self._repository.save(reservation)
        return reservation