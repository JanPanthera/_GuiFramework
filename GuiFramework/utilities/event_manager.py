from collections import defaultdict
from GuiFramework.utilities.utils import setup_default_logger
import threading


class EventManager:
    """A class for managing events and their subscribers."""
    logger = setup_default_logger("EventManager")
    subscribers = defaultdict(set)
    lock = threading.RLock()

    @classmethod
    def subscribe(cls, event_type, callback):
        """Subscribes a callback to an event type."""
        if not callable(callback):
            cls.logger.error("Callback is not callable: %s", callback)
            return
        with cls.lock:
            cls.subscribers[event_type].add(callback)

    @classmethod
    def unsubscribe(cls, event_type, callback):
        """Unsubscribes a callback from an event type."""
        with cls.lock:
            cls.subscribers[event_type].discard(callback)

    @classmethod
    def notify(cls, event_type, *args, **kwargs):
        """Notifies all subscribers of an event type."""
        callbacks = cls.subscribers.get(event_type, [])
        if not callbacks:
            return
        with cls.lock:
            callbacks = list(callbacks)
        for callback in callbacks:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                cls.logger.error("Error notifying subscriber: %s", e)
