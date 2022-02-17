from typing import Any, Callable
from attrs import define, field
from pymonad.tools import curry
from pymonad.reader import Pipe
from pyfuncify import fn

@define
class Observers:
    observers: list = field(default=[])

    def observers_for_event(self, event):
        return (Pipe(self.observers)
                .then(self.matching_observers(event))
                .then(self.extract_observer_fn)
                .flush())

    @curry(3)
    def matching_observers(self, event, observers):
        return fn.select(self.event_predicate(event), observers)

    @curry(2)
    def extract_observer_fn(self, matched_observers):
        return [obs.observer_fn for obs in matched_observers]

    @curry(3)
    def event_predicate(self, event, observer):
        return observer.event == event


@define
class Observer:
    event: Any
    observer_fn: Callable

def observers_for_event(event: Any, observers: Observers):
    return observers.observers_for_event(event)