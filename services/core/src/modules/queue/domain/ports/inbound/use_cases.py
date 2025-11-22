from shared.building_blocks import UseCase
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


ICreateQueue = UseCase[CreateQueue, Queue]

IChangeName = UseCase[ChangeName, None]

IChangeDescription = UseCase[ChangeDescription, None]

IChangeCleanupPeriod = UseCase[ChangeCleanupPeriod, None]

ICleanupQueue = UseCase[CleanupQueue, None]

IToggleQueueActivity = UseCase[ToggleQueueActivity, None]

IActivateQueue = UseCase[ActivateQueue, None]

IDeactivateQueue = UseCase[DeactivateQueue, None]
