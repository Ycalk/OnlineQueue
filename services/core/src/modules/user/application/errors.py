from shared.building_blocks.errors import ApplicationError


class UserNotFoundError(ApplicationError): ...


class UserAlreadyExistsError(ApplicationError): ...
