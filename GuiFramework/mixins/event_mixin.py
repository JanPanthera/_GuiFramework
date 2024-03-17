# GuiFramework/mixins/event_mixin.py

from GuiFramework.utilities import EventManager


class EventMixin:
    """Mixin to add event subscription capabilities to a class."""

    def __init__(self):
        # You can optionally initialize mixin-specific data here
        pass

    def subscribe(self, event_type, callback):
        """Subscribe to an event with a callback."""
        EventManager.subscribe(event_type, callback)

    def unsubscribe(self, event_type, callback):
        """Unsubscribe from an event."""
        EventManager.unsubscribe(event_type, callback)

    def notify(self, event_type, *args, **kwargs):
        """Notify all subscribers of an event."""
        EventManager.notify(event_type, *args, **kwargs)