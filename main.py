import time
from synth import SynthWrapper
from dispatcher import EventDispatcher
from midi_input import MidiInput


def main():
    dispatcher = EventDispatcher()
    synth = SynthWrapper()
    midi_in = MidiInput(dispatcher)

    dispatcher.register(synth.on_midi_event)

    try:
        while True:
            midi_in.poll()
            time.sleep(0.005)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
