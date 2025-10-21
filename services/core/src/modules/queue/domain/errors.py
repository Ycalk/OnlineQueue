from shared.building_blocks import DomainError


class CannotChangeSlotDuration(DomainError): ...


class CannotDeactivateAlreadyDeactivatedQueue(DomainError): ...


class CannotActivateAlreadyActiveQueue(DomainError): ...
