from typing import Self


class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ApplicationException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class CustomHTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        error: str,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        self.status_code = status_code
        self.error = error
        self.message = message
        self.headers = headers

    @classmethod
    def from_exception(
        cls,
        exc: DomainException | ApplicationException,
        status_code: int = 400,
        headers: dict[str, str] | None = None,
    ) -> Self:
        return cls(
            status_code=status_code,
            error=exc.__class__.__name__,
            message=exc.message,
            headers=headers,
        )
