# pet_utils.py
import json
import os

DATA_DIR = "data"
PETS_FILE = os.path.join(DATA_DIR, "pets.json")


def load_pets():
    if not os.path.exists(PETS_FILE):
        print("Hmm... I think all the pets are hiding right now.")
        return []
    with open(PETS_FILE, "r") as f:
        pets = json.load(f)
        if not pets:
            print("Hmm... I think all the pets are hiding right now.")
        return pets


def save_pets(pets):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PETS_FILE, "w") as f:
        json.dump(pets, f, indent=2)


def update_pet(updated_pet):
    """
    Updates a single pet in the saved list based on a unique identifier.
    Returns True if updated, False if pet not found.
    """
    pets = load_pets()
    for i, pet in enumerate(pets):
        # Use name + spawn_date as a unique identifier
        if pet["name"] == updated_pet["name"] and pet["spawn_date"] == updated_pet["spawn_date"]:
            pets[i] = updated_pet
            save_pets(pets)
            return True
    return False
