# GuiFramework/mixins/event_mixin.py

import uuid
import threading

from collections import defaultdict
from typing import Callable, Dict, Set


def create_event_type_id() -> str:
    """Generate and return a new unique event type id."""
    return str(uuid.uuid4())


class EventMixin:
    def __init__(self):
        """Initialize the event mixin with default values."""
        self._subscribers: Dict[str, Set[Callable]] = defaultdict(set)
        self._lock = threading.RLock()

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe a callback to a specified event type."""
        if not callable(callback):
            raise ValueError(f"Callback is not callable: {callback}")
        with self._lock:
            self._subscribers[event_type].add(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe a callback from a specified event type."""
        with self._lock:
            self._subscribers[event_type].discard(callback)

    def notify(self, event_type: str, *args, **kwargs) -> None:
        """Notify all subscribers of a specified event type."""
        with self._lock:
            callbacks = list(self._subscribers[event_type])
        for callback in callbacks:
            callback(event_type, *args, **kwargs)


class StaticEventMixin:
    _subscribers: Dict[str, Set[Callable]] = defaultdict(set)
    _lock = threading.RLock()

    @classmethod
    def subscribe(cls, event_type: str, callback: Callable) -> None:
        """Subscribe a callback to a specified event type, statically."""
        if not callable(callback):
            raise ValueError(f"Callback is not callable: {callback}")
        with cls._lock:
            cls._subscribers[event_type].add(callback)

    @classmethod
    def unsubscribe(cls, event_type: str, callback: Callable) -> None:
        """Unsubscribe a callback from a specified event type, statically."""
        with cls._lock:
            cls._subscribers[event_type].discard(callback)

    @classmethod
    def notify(cls, event_type: str, *args, **kwargs) -> None:
        """Notify all subscribers of a specified event type, statically."""
        with cls._lock:
            callbacks = list(cls._subscribers[event_type])
        for callback in callbacks:
            callback(event_type, *args, **kwargs)
