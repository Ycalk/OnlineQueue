from abc import ABC
from .domain_event import DomainEvent
from dataclasses import dataclass, field


@dataclass
class AggregateRoot(ABC):
    _domain_events: list[DomainEvent] = field(
        default_factory=list, init=False, repr=False
    )

    @property
    def events(self) -> list[DomainEvent]:
        return self._domain_events

    def _add_event(self, event: DomainEvent):
        self._domain_events.append(event)
