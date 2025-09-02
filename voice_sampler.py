# voice_sampler.py
import json
import os
import math
import wave
from datetime import datetime

# --- Configuration ---
DATA_FILE = "data/pets.json"
OUTPUT_DIR = "audio_samples"

# Audio settings
SAMPLE_RATE = 44100  # Samples per second
AMPLITUDE = 16000    # Volume (max is 32767 for 16-bit audio)
NOTE_DURATION = 0.18 # Seconds per character beep
GAP_DURATION = 0.07  # Seconds of silence between beeps
WORD_PAUSE = 0.5     # Seconds of silence between words

# Character to frequency mapping (from voice.py)
CHAR_TO_FREQ = {
    "a": 261.63, "s": 293.66, "d": 329.63, "f": 349.23,
    "g": 392.00, "h": 440.00, "j": 493.88, "k": 523.25,
}

# --- Helper Functions ---
def load_pets():
    """Loads all pets from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def select_pet(pets):
    """Prompts the user to select a pet from a list."""
    print("Select a pet to create a voice sample for:")
    for i, pet in enumerate(pets, 1):
        status = " (released)" if pet.get("released") else ""
        print(f"  {i}. {pet['name']}{status}")
    
    choice = input("Your choice: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(pets):
        return pets[int(choice) - 1]
    print("Invalid selection.")
    return None

def generate_wave_data(frequency, duration):
    """Generates raw byte data for a sine wave."""
    num_samples = int(duration * SAMPLE_RATE)
    data = bytearray()
    for i in range(num_samples):
        angle = 2 * math.pi * i * frequency / SAMPLE_RATE
        sample = int(AMPLITUDE * math.sin(angle))
        # Convert to 16-bit signed little-endian bytes
        data += sample.to_bytes(2, byteorder='little', signed=True)
    return data

def save_wav_file(pet_name, audio_data):
    """Saves the combined audio data to a .wav file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{pet_name.replace(' ', '_')}_vocab_{datetime.now().strftime('%Y%m%d')}.wav"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 16-bit audio (2 bytes per sample)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data)
        
    print(f"\n✅ Success! Audio sample saved to: {filepath}")

# --- Main Execution ---
def main():
    """Main function to run the voice sampler."""
    pets = load_pets()
    if not pets:
        print("No pets found. Create a pet in the main app first!")
        return
        
    selected_pet = select_pet(pets)
    if not selected_pet:
        return
        
    print(f"\nGenerating voice sample for {selected_pet['name']}...")

    words_to_speak = selected_pet.get("words", [selected_pet.get("word", "")])
    full_audio = bytearray()
    
    # Generate silence data for pauses
    gap_audio = generate_wave_data(0, GAP_DURATION)
    word_pause_audio = generate_wave_data(0, WORD_PAUSE)

    for i, word in enumerate(words_to_speak):
        for char in word.lower():
            freq = CHAR_TO_FREQ.get(char, 440.0) # Default to 440 Hz
            full_audio.extend(generate_wave_data(freq, NOTE_DURATION))
            full_audio.extend(gap_audio)
        
        # Add a longer pause between words, but not after the last one
        if i < len(words_to_speak) - 1:
            full_audio.extend(word_pause_audio)

    if not full_audio:
        print("This pet doesn't know any words to sample!")
        return

    save_wav_file(selected_pet['name'], full_audio)

if __name__ == "__main__":
    main()