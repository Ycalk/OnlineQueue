from shared.building_blocks.errors import ApplicationException


class UserNotFoundError(ApplicationException): ...


class UserAlreadyExistsError(ApplicationException): ...
