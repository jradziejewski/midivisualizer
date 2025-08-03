from dataclasses import dataclass


@dataclass
class MidiEvent:
    timestamp: float
    note: int
    velocity: int
    type: str  # 'note_on' or 'note_off

    def __repr__(self):
        return f"NOTE: {self.note}, VEL: {self.velocity}, TYPE: {self.type}, AT: {self.timestamp}"
