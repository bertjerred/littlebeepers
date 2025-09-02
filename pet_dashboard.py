# pet_dashboard.py
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "data/pets.json"
REPORT_DIR = "reports"

def load_pets():
    """Loads all pets from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def format_timedelta(delta: timedelta) -> str:
    """Formats a timedelta object into a human-readable string."""
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts: # Show seconds if it's the only unit
        parts.append(f"{seconds}s")
        
    return " ".join(parts) if parts else "0s"

def display_summary(pets):
    """Prints a high-level summary of the entire pet collection."""
    print("--- 🐾 Pet Collection Dashboard 🐾 ---")
    if not pets:
        print("No pets found. Create one in the main app first!")
        return

    total_pets = len(pets)
    active_pets = sum(1 for p in pets if not p.get("released"))
    released_pets = total_pets - active_pets
    
    total_time_spent = sum(h.get("duration_seconds", 0) for p in pets for h in p.get("history", []))
    total_time_delta = timedelta(seconds=total_time_spent)

    print(f"Total Pets:      {total_pets} ({active_pets} active, {released_pets} released)")
    print(f"Total Time Spent:  {format_timedelta(total_time_delta)}")
    print("-" * 38 + "\n")

def generate_pet_report(pet: dict) -> str:
    """Generates a detailed, multi-line string report for a single pet."""
    report_lines = []
    now = datetime.now()

    # --- Basic Info & Status ---
    spawn_date = datetime.fromisoformat(pet["spawn_date"])
    age = now - spawn_date
    status = "Released" if pet.get("released") else "Active"
    
    report_lines.append(f"# Status Report for {pet['name']}")
    report_lines.append(f"**Species:** {pet['species']} | **Status:** {status}")
    report_lines.append(f"**Age:** {format_timedelta(age)}")

    # --- Interaction Stats ---
    history = pet.get("history", [])
    last_interaction_str = "Never"
    if history:
        last_timestamp = datetime.fromisoformat(history[-1]["timestamp"])
        time_since = now - last_timestamp
        last_interaction_str = f"{format_timedelta(time_since)} ago"
    
    total_seconds = sum(h.get("duration_seconds", 0) for h in history)
    
    report_lines.append(f"**Last Interaction:** {last_interaction_str}")
    report_lines.append(f"**Total Time Spent:** {format_timedelta(timedelta(seconds=total_seconds))}")

    # --- Words & Learning ---
    words = pet.get("words", [pet.get("word")])
    report_lines.append(f"\n## Vocabulary ({len(words)} words known)")
    report_lines.append(f"Words: `{'`, `'.join(words)}`")

    # --- Playdate Analysis ---
    playdates = [h for h in history if h.get("event") == "playdate"]
    partners = {partner for pd in playdates for partner in pd.get("partners", [])}
    report_lines.append(f"\n## Social History")
    report_lines.append(f"**Playdates Attended:** {len(playdates)}")
    if partners:
        report_lines.append(f"**Has played with:** {', '.join(sorted(list(partners)))}")
    else:
        report_lines.append("**Has played with:** No one yet")
    
    return "\n".join(report_lines)

def save_report(pet_name: str, content: str):
    """Saves the generated report content to a Markdown file."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"{pet_name.replace(' ', '_')}_status_{datetime.now().strftime('%Y%m%d')}.md"
    filepath = os.path.join(REPORT_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"\n✅ Report saved successfully to: {filepath}")

def main():
    """Main function to run the dashboard."""
    all_pets = load_pets()
    display_summary(all_pets)

    if not all_pets:
        return

    while True:
        print("Select a pet for a detailed report:")
        for i, pet in enumerate(all_pets, 1):
            print(f"  {i}. {pet['name']}")
        print("  Q. Quit")

        choice = input("Your choice: ").strip().lower()

        if choice == 'q':
            break
        
        if choice.isdigit() and 1 <= int(choice) <= len(all_pets):
            selected_pet = all_pets[int(choice) - 1]
            
            print("\n" + "="*50)
            report_content = generate_pet_report(selected_pet)
            print(report_content)
            print("="*50 + "\n")
            
            save_choice = input("Save this report to a file? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_report(selected_pet['name'], report_content)
            print("\nReturning to selection...\n")
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()