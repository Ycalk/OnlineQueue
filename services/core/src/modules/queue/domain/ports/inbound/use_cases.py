from shared.building_blocks import DomainUseCase
from modules.queue.domain.commands import (
    ActivateQueue,
    ChangeCleanupPeriod,
    ChangeDescription,
    ChangeName,
    CleanupQueue,
    CreateQueue,
    DeactivateQueue,
    ToggleQueueActivity,
)
from modules.queue.domain.aggregates import Queue


ICreateQueue = DomainUseCase[CreateQueue, Queue]

IChangeName = DomainUseCase[ChangeName, None]

IChangeDescription = DomainUseCase[ChangeDescription, None]

IChangeCleanupPeriod = DomainUseCase[ChangeCleanupPeriod, None]

ICleanupQueue = DomainUseCase[CleanupQueue, None]

IToggleQueueActivity = DomainUseCase[ToggleQueueActivity, None]

IActivateQueue = DomainUseCase[ActivateQueue, None]

IDeactivateQueue = DomainUseCase[DeactivateQueue, None]
