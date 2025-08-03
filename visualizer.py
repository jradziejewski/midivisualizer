import pygame
from dispatcher import MidiEvent

BASE_NOTE = 60  # C4
NUM_OCTAVES = 2
WHITE_KEY_WIDTH = 40
WHITE_KEY_HEIGHT = 180
BLACK_KEY_WIDTH = 24
BLACK_KEY_HEIGHT = 100

BLACK_KEY_OFFSETS = {
    1: 0.75,  # C#
    3: 1.75,  # D#
    6: 3.25,  # F#
    8: 4.25,  # G#
    10: 5.25,  # A#
}

WHITE_NOTES_IN_OCTAVE = [0, 2, 4, 5, 7, 9, 11]  # C, D, E, F, G, A, B


class Visualizer:
    def __init__(self):
        pygame.init()
        total_white = NUM_OCTAVES * 7
        width = total_white * WHITE_KEY_WIDTH
        height = WHITE_KEY_HEIGHT

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("MIDI Visualizer")
        self.clock = pygame.time.Clock()

        self.active_notes = set()

        self.white_keys = []
        self.black_keys = []
        self._build_key_geometry()

    def _build_key_geometry(self):
        for octave in range(NUM_OCTAVES):
            for i, offset in enumerate(WHITE_NOTES_IN_OCTAVE):
                note = BASE_NOTE + octave * 12 + offset
                x = (octave * 7 + i) * WHITE_KEY_WIDTH
                rect = pygame.Rect((x, 0, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT))
                self.white_keys.append((note, rect))

        for octave in range(NUM_OCTAVES):
            for semitone_offset, rel in BLACK_KEY_OFFSETS.items():
                note = BASE_NOTE + octave * 12 + semitone_offset
                x = (octave * 7 + rel) * WHITE_KEY_WIDTH - (BLACK_KEY_WIDTH / 2)
                rect = pygame.Rect(int(x), 0, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)
                self.black_keys.append((note, rect))

    def on_midi_event(self, event):
        if event.type == "note_on":
            self.active_notes.add(event.note)
        elif event.type == "note_off":
            self.active_notes.discard(event.note)

    def handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        self.screen.fill((100, 100, 100))

        for note, rect in self.white_keys:
            if note in self.active_notes:
                color = (255, 200, 100)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

        for note, rect in self.black_keys:
            if note in self.active_notes:
                color = (255, 150, 50)
            else:
                color = (0, 0, 0)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

        pygame.display.flip()
        self.clock.tick(60)


viz = Visualizer()


def main():
    while True:
        if not viz.handle_pygame_events():
            break
        viz.draw()

    pygame.quit()


if __name__ == "__main__":
    main()
