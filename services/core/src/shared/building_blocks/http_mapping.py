from http import HTTPStatus

EXCEPTION_STATUS_MAP: dict[str, int] = {
    "InvalidPasswordError": HTTPStatus.FORBIDDEN,
    "UserNotFoundError": HTTPStatus.NOT_FOUND,
    "UserAlreadyExistsError": HTTPStatus.CONFLICT,
    "QueueNotFoundError": HTTPStatus.NOT_FOUND,
    "NoRightsError": HTTPStatus.FORBIDDEN,
}


def get_status_code_for_exception(exc: Exception) -> int:
    exc_class_name = exc.__class__.__name__

    if exc_class_name in EXCEPTION_STATUS_MAP:
        return EXCEPTION_STATUS_MAP[exc_class_name]

    from .errors import DomainException, ApplicationException

    if isinstance(exc, DomainException) or isinstance(exc, ApplicationException):
        return HTTPStatus.BAD_REQUEST

    return HTTPStatus.INTERNAL_SERVER_ERROR
