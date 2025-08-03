import time
import mido  # type: ignore
from dispatcher import MidiEvent


class MidiInput:
    def __init__(self, dispatcher, device_index=0):
        inputs = mido.get_input_names()
        if not inputs:
            raise RuntimeError("No MIDI input devices found.")

        name = inputs[device_index]
        print(name)
        self.inport = mido.open_input(name)
        self.dispatcher = dispatcher
        print(f"Listening to MIDI input on device: {name}...")

    def poll(self):
        for msg in self.inport.iter_pending():
            if msg.type not in ("note_on", "note_off"):
                continue

            now = time.time()
            event = MidiEvent(
                timestamp=now, note=msg.note, velocity=msg.velocity, type=msg.type
            )
            self.dispatcher.dispatch(event)
