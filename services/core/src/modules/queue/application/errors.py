from shared.building_blocks.errors import ApplicationException


class QueueNotFoundError(ApplicationException): ...


class NoRightsError(ApplicationException): ...
