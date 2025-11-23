from abc import ABC
from typing import TypeVar, Protocol
from shared.building_blocks.aggregate_root import AggregateRoot
from shared.building_blocks.event import IEventPublisher


class ApplicationUseCase(ABC):
    def __init__(self, event_publisher: IEventPublisher):
        self._event_publisher = event_publisher

    async def _publish_events(self, aggregate: AggregateRoot):
        for event in aggregate.events:
            await self._event_publisher.publish(event)


TCommand_contra = TypeVar("TCommand_contra", contravariant=True)
TResult_co = TypeVar("TResult_co", covariant=True)


class DomainUseCase(Protocol[TCommand_contra, TResult_co]):
    async def __call__(self, command: TCommand_contra) -> TResult_co: ...


TQueryData_contra = TypeVar("TQueryData_contra", contravariant=True)
TQueryResult_co = TypeVar("TQueryResult_co", covariant=True)


class QueryUseCase(Protocol[TQueryData_contra, TQueryResult_co]):
    async def __call__(self, data: TQueryData_contra) -> TQueryResult_co: ...
