class RequestDomainError(Exception):
    """Базовое исключение для bounded context request."""


class TimePeriodNotValid(RequestDomainError):
    """Неверный интервал времени (start > end)."""
