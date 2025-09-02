import pygame
import time
import math

# Map characters to frequencies (Hz) like before
CHAR_TO_FREQ = {
    "a": 261.63,  # C4
    "s": 293.66,  # D4
    "d": 329.63,  # E4
    "f": 349.23,  # F4
    "g": 392.00,  # G4
    "h": 440.00,  # A4
    "j": 493.88,  # B4
    "k": 523.25,  # C5
}

def speak_word(word: str):
    """Play the pet's word as short beeps using pygame."""
    pygame.mixer.init(frequency=44100, size=-16, channels=1)
    
    for char in word.lower():
        freq = CHAR_TO_FREQ.get(char, 440.0)  # fallback A4
        beep = make_beep(freq, 0.2)  # 0.2 seconds per beep
        beep.play()
        time.sleep(0.25)  # small gap between notes
    
    pygame.mixer.quit()

def make_beep(frequency, duration):
    """Generate a beep sound as a pygame Sound object."""
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate))
    buf = bytearray()

    volume = 32767
    for s in range(n_samples):
        t = float(s) / sample_rate
        val = int(volume * 0.5 * (1 + math.sin(2.0 * math.pi * frequency * t)))
        buf += val.to_bytes(2, byteorder="little", signed=True)

    return pygame.mixer.Sound(buffer=bytes(buf))
