import time
from synth import SynthWrapper
from dispatcher import EventDispatcher
from midi_input import MidiInput
from visualizer import Visualizer


def main():
    dispatcher = EventDispatcher()
    synth = SynthWrapper()
    visualizer = Visualizer()

    dispatcher.register(synth.on_midi_event)
    dispatcher.register(visualizer.on_midi_event)

    midi_in = MidiInput(dispatcher)

    try:
        while True:
            midi_in.poll()
            time.sleep(0.005)

            if not visualizer.handle_pygame_events():
                break
            visualizer.draw()
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
