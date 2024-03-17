# GuiFramework/utilities/event_manager.py

import threading

from collections import defaultdict
from GuiFramework.utilities.logging import Logger


class EventManager:
    logger = Logger.get_logger("GuiFramework")
    subscribers = defaultdict(set)
    lock = threading.RLock()

    @classmethod
    def subscribe(cls, event_type, callback):
        """Subscribes a callback to an event type."""
        if not callable(callback):
            cls.logger.log_error(f"Callback is not callable: {callback}", "EventManager")
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
                callback(event_type, *args, **kwargs)
            except Exception as e:
                cls.logger.log_error(f"Error notifying subscriber: {e}", "EventManager")
