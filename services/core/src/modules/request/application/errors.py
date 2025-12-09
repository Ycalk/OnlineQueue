from shared.building_blocks.errors import ApplicationException


class RequestNotFoundError(ApplicationException): ...


class NoRightsError(ApplicationException): ...
