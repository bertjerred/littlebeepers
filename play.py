# play.py
import random
import time
from datetime import datetime
from voice import speak_word
from pet_utils import load_pets, update_pet

def host_playdate():
    # Filter out released pets from being available for playdates.
    all_pets = load_pets()
    active_pets = [p for p in all_pets if not p.get("released")]
    
    if len(active_pets) < 2:
        print("You need at least 2 active (not released) pets to host a playdate!")
        return

    # Sequential selection of pets
    playdate_pets = []
    while True:
        print("\nAvailable pets:")
        # Display only pets that are not already chosen for the current playdate
        available_for_selection = [p for p in active_pets if p not in playdate_pets]
        for i, pet in enumerate(available_for_selection, start=1):
            print(f"{i}. {pet['name']} ({pet['species']})")

        choice = input("Choose a pet by number (Enter to stop adding): ").strip()
        if not choice:
            break
        if choice.isdigit() and 1 <= int(choice) <= len(available_for_selection):
            selected = available_for_selection[int(choice) - 1]
            if selected not in playdate_pets:
                playdate_pets.append(selected)
                print(f"Added {selected['name']} to the playdate!")
            else:
                print("That pet is already on the list!") # This case should not be reachable now
        else:
            print("Invalid choice.")

    if len(playdate_pets) < 2:
        print("Not enough pets selected. Playdate canceled.")
        return

    print("\n🎉 The playdate begins! Type 'end' anytime to finish.\n")
    start_time = time.time()
    turn_order = playdate_pets[:]
    random.shuffle(turn_order)
    index = 0

    while True:
        pet = turn_order[index]
        word = random.choice(pet.get("words", [pet.get("word")]))
        print(f"{pet['name']} says: {word}")
        speak_word(word)

        # Move to next pet, reshuffle if looped
        index = (index + 1) % len(turn_order)
        if index == 0:
            random.shuffle(turn_order)

        cmd = input("(Press Enter to continue, or type 'end' to finish): ").strip().lower()
        if cmd == "end":
            duration_seconds = int(time.time() - start_time)
            conclude_playdate(playdate_pets, duration_seconds)
            return


def conclude_playdate(playdate_pets, duration_seconds):
    print("\nProcessing new friendships...")
    spinner()

    # Gather all letters from all pets' words
    all_letters = []
    for pet in playdate_pets:
        if "words" in pet:
            for w in pet["words"]:
                all_letters.extend(list(w))
        elif "word" in pet:
            all_letters.extend(list(pet["word"]))

    for pet in playdate_pets:
        new_word = "".join(random.choice(all_letters) for _ in range(5))
        pet.setdefault("words", [])
        if "word" in pet and pet["word"] not in pet["words"]:
            pet["words"].append(pet["word"])
            del pet["word"]
        pet["words"].append(new_word)

        print(f"{pet['name']} learned a new word: {new_word}")
        speak_word(new_word)

        # Log playdate participation
        pet.setdefault("history", []).append({
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": duration_seconds,
            "event": "playdate",
            "partners": [p["name"] for p in playdate_pets if p is not pet]
        })

        # Save each pet individually
        update_pet(pet)

    print("\n✅ Playdate ended and logged successfully!\n")


def spinner():
    for _ in range(3):
        for dots in [".", "..", "..."]:
            print(f"Processing{dots}", end="\r")
            time.sleep(0.5)
    print(" " * 20, end="\r")