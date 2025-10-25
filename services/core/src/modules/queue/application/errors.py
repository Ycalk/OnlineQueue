from shared.building_blocks.errors import ApplicationError


class QueueNotFoundError(ApplicationError): ...


class NoRightsError(ApplicationError): ...
