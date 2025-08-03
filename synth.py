import numpy as np
import sounddevice as sd
import threading
import time
from math import sin, pi

SAMPLE_RATE = 44100
BUFFER_SIZE = 1024


def note_to_frequency(note):
    """Convert MIDI note number to frequency."""
    return 440.0 * (2 ** ((note - 69) / 12))


class Synthesizer:
    def __init__(self):
        self.active_notes = {}
        self.lock = threading.Lock()
        self.stream = sd.OutputStream(
            sample_rate=SAMPLE_RATE,
            channels=1,
            blocksize=BUFFER_SIZE,
            callback=self.audio_callback,
        )
        self.stream.start()

    def audio_callback(self, outdata, frames, time_info, status):
        # Time Axis
        t = (np.arange(frames) / SAMPLE_RATE).astype(np.float32)

        # Buffer for notes sound waves
        samples = np.zeros(frames, dtype=np.float32)

        with self.lock:  # Lock to ensure active_notes is not modified during processing
            notes = list(self.active_notes.items())
            for note, phase in notes:
                # Generate wave for each active note
                freq = note_to_frequency(note)
                wave = np.sin(2 * np.pi * freq * t + phase)

                samples += wave * 0.2  # volume control

                # Calculate the starting phase the next buffer - advance phase by the angular distance travelled in this buffer and wrap to [0, 2π)
                self.active_notes[note] = (
                    phase + 2 * np.pi * freq * frames / SAMPLE_RATE
                ) % (2 * np.pi)

        # Avoid clipping (multiple waves together can get loud)
        samples = np.clip(samples, -1, 1)

        # Write the samples to the output stream
        outdata[:] = samples.reshape(-1, 1)
