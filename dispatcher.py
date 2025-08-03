from dataclasses import dataclass
import threading


@dataclass
class MidiEvent:
    timestamp: float
    note: int
    velocity: int
    type: str  # 'note_on' or 'note_off

    def __repr__(self):
        return f"NOTE: {self.note}, VEL: {self.velocity}, TYPE: {self.type}, AT: {self.timestamp}"


class EventDispatcher:
    def __init__(self):
        self._subscribers = []
        self._lock = threading.Lock()

    def register(self, callback):
        with self._lock:
            self._subscribers.append(callback)

    def unregister(self, callback):
        with self._lock:
            if callback in self._subscribers:
                self._subscribers.remove(callback)

    def dispatch(self, event):
        with self._lock:
            subs = list(self._subscribers)
        for cb in subs:
            try:
                cb(event)
            except Exception as e:
                print(f"Error in subscriber {cb}: {e}")
