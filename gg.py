import pygame
import numpy as np
import sys

# ---------- CONFIG ----------
SAMPLE_RATE = 44100
DURATION = 1.5
STRING_COUNT = 6
FRET_COUNT = 12
WIDTH = 900
HEIGHT = 400
# ----------------------------

pygame.init()
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Guitar Simulator")

# Standard tuning frequencies (E2 A2 D3 G3 B3 E4)
open_strings = [
    82.41,   # E2
    110.00,  # A2
    146.83,  # D3
    196.00,  # G3
    246.94,  # B3
    329.63   # E4
]

def generate_string_sound(freq):
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)

    # Basic plucked string sound (decay envelope)
    wave = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-3 * t)
    sound = wave * envelope

    audio = (sound * 32767).astype(np.int16)

    # Convert to stereo
    stereo = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo)

# Pre-generate sounds for all frets
sounds = []
for string_freq in open_strings:
    string_sounds = []
    for fret in range(FRET_COUNT + 1):
        freq = string_freq * (2 ** (fret / 12))
        string_sounds.append(generate_string_sound(freq))
    sounds.append(string_sounds)

# Draw guitar fretboard
string_spacing = HEIGHT // (STRING_COUNT + 1)
fret_spacing = WIDTH // (FRET_COUNT + 1)

running = True
while running:
    screen.fill((139, 69, 19))  # Wood color

    # Draw frets
    for fret in range(FRET_COUNT + 1):
        x = fret * fret_spacing
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT), 3)

    # Draw strings
    for i in range(STRING_COUNT):
        y = (i + 1) * string_spacing
        pygame.draw.line(screen, (220, 220, 220), (0, y), (WIDTH, y), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            fret = x // fret_spacing
            string = y // string_spacing

            if 0 <= string < STRING_COUNT and 0 <= fret <= FRET_COUNT:
                sounds[string][fret].play()

    pygame.display.flip()

pygame.quit()
sys.exit()
