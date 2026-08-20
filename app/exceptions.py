class ReservationError(Exception):
    """Custom exception for reservation-related errors."""
    pass


class InvalidCustomerError(ReservationError):
    """Exception raised for invalid customer data."""
    pass

class InvalidServiceError(ReservationError):
    """Exception raised for invalid service data."""
    pass

class InvalidDurationError(ReservationError):
    """Exception raised for invalid duration data."""
    pass

class InvalidReservationDateError(ReservationError):
    """Exception raised for invalid reservation date."""
    pass

class InvalidReservationTimeError(ReservationError):
    """Exception raised for invalid reservation time."""
    pass

class DuplicateReservationError(ReservationError):
    """Exception raised for duplicate reservations."""
    pass

InvalidCustomerNameError = InvalidCustomerError