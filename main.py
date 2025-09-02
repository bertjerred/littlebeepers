import random
import time
import json
from datetime import datetime
from voice import speak_word
from pet_utils import load_pets, save_pets


def create_pet():
    name = input("Enter a name for your new pet: ").strip() or "Unnamed Pet"
    species = "Little Beeper"

    # Generate the spawn-time secret word
    word = "".join(random.choice("asdfghjk") for _ in range(5))

    new_pet = {
        "name": name,
        "species": species,
        "spawn_date": datetime.now().isoformat(),
        "released": False,
        "history": [],
        "word": word,
        # I don't really have a use for these traits yet. Maybe I'll think of something later.
        "traits": {
            "vowel-loving": 5,
            "consonant-curious": 5,
            "punctuation-centric": 5
        }
    }

    pets = load_pets()
    pets.append(new_pet)
    save_pets(pets)

    print(f"\n✨ {name} the {species} has joined your collection!")
    print(f"They already know a secret word: {word}")
    speak_word(word) # The secret word is played once upon creation.


def log_visit(pet, duration_seconds):
    pet.setdefault("history", [])
    pet["history"].append({
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration_seconds
    })


def visit_pet(pet):
    print(f"\n--- Visiting {pet['name']} the {pet['species']} ---")
    start_time = time.time()
    
    while True:
        print("\nOptions:")
        print("1. View pet details")
        print("2. Ask pet to speak")
        print("3. Release pet")
        print("4. Return to main menu")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            print(json.dumps(pet, indent=2))
        elif choice == "2":
            # Support multiple words if present
            if "words" in pet:
                word = random.choice(pet["words"])
            else:
                word = pet.get("word", "[silent]")

            print(f"\n{pet['name']} speaks a word it knows: {word}") # Text changed for clarity.
            speak_word(word)
        elif choice == "3":
            print(f"\nReleasing a pet is permanent. They will be free to explore the world on their own.")
            confirm = input(f"Are you sure you want to release {pet['name']}? (type 'yes' to confirm): ").strip().lower()
            if confirm == 'yes':
                pet['released'] = True
                from pet_utils import update_pet
                update_pet(pet)
                print(f"\n{pet['name']} beeps thankfully for the wonderful time you spent together.")
                print("It is thrilled to go explore on its own. Goodbye, friend! 👋")
                time.sleep(2) # Pause to let the message sink in.
                return # Exit the visit
            else:
                print("Release cancelled.")

        elif choice == "4":
            break
        else:
            print("Oops, let's try that again.")

    duration_seconds = int(time.time() - start_time)
    log_visit(pet, duration_seconds)

    # Update the pet safely
    from pet_utils import update_pet
    update_pet(pet)

    print(f"\n✅ Interaction of {duration_seconds} seconds recorded.\n")

def select_pet():
    pets = load_pets()
    if not pets:
        return None

    print("\nWhich pet would you like to visit?")
    for i, pet in enumerate(pets, start=1):
        status = "released" if pet.get("released") else "active"
        print(f"{i}. {pet['name']} ({pet['species']}, {status})")

    choice = input("Choose a pet by number (or press Enter to cancel): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(pets):
        selected_pet = pets[int(choice) - 1]
        if selected_pet.get("released"):
            print(f"\n{selected_pet['name']} has already been released and cannot be visited.")
            return None
        return selected_pet
    else:
        print("Cancelled or invalid selection.")
        return None


def host_playdate_option():
    # Local import to avoid circular import
    from play import host_playdate
    host_playdate()


def main():
    print("\n👾 Welcome to Little Beepers!")
    print("Discover and care for your own unique sound-making companions. What will they have to say?")
    print("Find out more at https://github.com/bertjerred/littlebeepers\n")

    while True:
        print("=== Main Menu ===")
        print("1. Create a new pet")
        print("2. Visit an existing pet")
        print("3. Host a playdate")
        print("4. Exit")

        choice = input("What would you like to do? ").strip()
        if choice == "1":
            create_pet()
        elif choice == "2":
            pet = select_pet()
            if pet:
                visit_pet(pet)
        elif choice == "3":
            host_playdate_option()
        elif choice == "4":
            print("\nGoodbye! Your pets will be happily entertaining themselves while you are away.\n")
            break
        else:
            print("Hmm... that doesn't seem right. Please try again.")


if __name__ == "__main__":
    main()