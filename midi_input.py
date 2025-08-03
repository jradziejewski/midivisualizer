import time
import mido  # type: ignore
from dispatcher import MidiEvent

inputs = mido.get_input_names()
inport = mido.open_input(inputs[0])


print(f"Listening to MIDI input on device: {inputs[0]}...")

while True:
    msg = inport.receive()
    if msg.type in ["note_on", "note_off"]:
        event = MidiEvent(time.time(), msg.note, msg.velocity, msg.type)
        print(event)
    elif KeyboardInterrupt:
        break
