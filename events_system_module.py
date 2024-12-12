class GameEvent:
    def __init__(self, event_type, payload=None):
        self.event_type = event_type
        self.payload = payload

class EventType:
    CARD_PLAYED = "CardPlayed"
    CARD_SOLD = "CardSold"
    TURN_START = "TurnStart"
    TURN_END = "TurnEnd"

class EventManager:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)

    def emit(self, event):
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                callback(event)



