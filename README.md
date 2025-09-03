# Little Beepers 🔈

A minimalist, text-based virtual pet game where you create, care for, and listen to unique sound-making companions.

---
## About the Project

**Little Beepers** is a simple, command-line virtual pet experience built with Python. Instead of visual pets, you interact with "beepers"—small companions that communicate through unique sequences of sounds, or "words." The mood is quiet, gentle, and focused on companionship and auditory growth. Create a new friend, listen to its secret sound, and host playdates to watch its vocabulary evolve.

---
## Features

* **Create Pets**: Generate new Little Beepers, each with a unique, randomly generated "secret word."
* **Visit & Interact**: Spend time with your pets, view their details, and ask them to speak.
* **Host Playdates**: Bring two or more pets together to socialize. They'll listen to each other and learn new words based on the sounds they hear!
* **Permanent Release**: When the time is right, you can release a pet to explore the world on its own in a heartfelt goodbye.
* **Persistent Data**: All your pets and their histories are saved locally in a `pets.json` file.

---
## Looking for precompiled executables?

You can find them [here](https://github.com/bertjerred/littlebeepers/releases).

## Or, just go straight Python:

Follow these steps to get your own Little Beepers running on your local machine.

### **Prerequisites**

* **Python 3.6+**
* **pip** (Python package installer)

### **Installation**

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/bertjerred/littlebeepers.git
    cd littlebeepers
    ```

2.  **Install the required package:**
    The project uses `pygame` for real-time audio playback.
    ```sh
    pip install pygame
    ```

3.  **Run the main game:**
    ```sh
    python main.py
    ```
    This will launch the application in your terminal. All pet data will be stored in a `data/` directory that is created automatically.

---
## Extra Tools 🛠️

This project includes two powerful, standalone utility scripts that run outside of the main game.

### **Pet Dashboard (`pet_dashboard.py`)**

This script is a comprehensive reporting tool for viewing the status of your entire pet collection.

* **How to run:**
    ```sh
    python pet_dashboard.py
    ```
* **Features:**
    * Displays a high-level **summary** of your collection (total pets, active vs. released, etc.).
    * Generates detailed **individual reports** including age, time since last interaction, and a full social history of playdates.
    * Saves these detailed reports as clean, readable **Markdown (`.md`) files** in a `reports/` directory.

### **Voice Sampler (`voice_sampler.py`)**

This script creates a miniature audio file of a selected pet's entire known vocabulary. It's a perfect way to capture and share your pet's unique voice.

* **How to run:**
    ```sh
    python voice_sampler.py
    ```
* **Features:**
    * Prompts you to select a pet from your collection.
    * Generates all the "beeps" for every word the pet knows.
    * Stitches the sounds together into a single, high-quality **`.wav` audio file**.
    * Saves the file to an `audio_samples/` directory.

---
## File Structure

* `main.py`: The main game application and user menu.
* `play.py`: Logic for hosting and managing playdates.
* `voice.py`: Real-time audio generation and playback using `pygame`.
* `pet_utils.py`: Helper functions for loading and saving pet data to `pets.json`.
* `pet_dashboard.py`: The standalone statistical reporting tool.
* `voice_sampler.py`: The standalone tool for generating `.wav` audio files.

## Donations
If you wish to make an optional donation, please do so [through PayPal](https://www.paypal.com/paypalme/bertjerred) or at my [Ko-Fi shop](https://ko-fi.com/bertjerred). Thank you.
