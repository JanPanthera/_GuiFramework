# GuiFramework/utilities/event_manager.py

import threading

from collections import defaultdict
from typing import Callable, Dict, Set


class EventManager:
    """Event manager for subscribing to and notifying events."""
    _subscribers: Dict[str, Set[Callable]] = defaultdict(set)
    _lock = threading.RLock()

    @classmethod
    def subscribe(cls, event_type: str, callback: Callable) -> None:
        """Subscribe to an event with a callback."""
        if not callable(callback):
            raise ValueError(f"Callback is not callable: {callback}")
        with cls._lock:
            cls._subscribers[event_type].add(callback)

    @classmethod
    def unsubscribe(cls, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event."""
        with cls._lock:
            cls._subscribers[event_type].discard(callback)

    @classmethod
    def notify(cls, event_type: str, *args, **kwargs) -> None:
        """Notify subscribers of an event."""
        with cls._lock:
            callbacks = list(cls._subscribers[event_type])
        for callback in callbacks:
            callback(event_type, *args, **kwargs)
