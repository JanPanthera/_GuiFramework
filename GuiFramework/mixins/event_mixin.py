import threading
from collections import defaultdict
from typing import Callable, Dict, Set


class EventMixin:
    def __init__(self):
        self._subscribers: Dict[str, Set[Callable]] = defaultdict(set)
        self._lock = threading.RLock()

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to an event with a callback."""
        if not callable(callback):
            raise ValueError(f"Callback is not callable: {callback}")
        with self._lock:
            self._subscribers[event_type].add(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event."""
        with self._lock:
            self._subscribers[event_type].discard(callback)

    def notify(self, event_type: str, *args, **kwargs) -> None:
        """Notify subscribers of an event."""
        with self._lock:
            callbacks = list(self._subscribers[event_type])
        for callback in callbacks:
            callback(event_type, *args, **kwargs)
