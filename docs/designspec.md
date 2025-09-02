# TextPet Minimal Design Specification

## Core Principles
- **Minimalism**: Small, simple, and purposeful. Avoid unnecessary complexity.
- **Efficiency**: Lightweight execution and storage. Fast startup, minimal dependencies.
- **Positivity**: Pets never die, only grow or can be released. Interactions reinforce a friendly, encouraging tone.
- **Clarity**: Always unmysterious. Straightforward navigation, transparent commands, no dead ends.
- **Command Line Only**: Text interface, no GUI. Commands are intuitive and predictable.
- **Modularity**: Engine, data, and interactions separated for easy maintenance and growth.
- **Hackability/Extensibility**: Clear file structures (JSON + modular code) that invite user modifications.

## Data Model
- **Template (`pet.json`)**: Defines the default attributes for a pet (species, base traits).
- **Pet Instances**: Each pet has:
  - Name (user-defined)
  - Spawn date (absolute age tracked)
  - Released status (true/false)
- **Persistence**: Pets are saved to disk as simple JSON, easily human-readable and editable.

## Interaction Model
- **Single Active Pet**: Only one pet is interacted with at a time.
- **Commands**: Minimal set at start (e.g., `new`, `list`, `select`, `info`, `release`).
- **Future Actions**: Feeding, playing, or other interactions can be added as modular commands.

## User Experience
- **Tone**: Always kind, never punishing. Pets are companions, not burdens.
- **Navigation**: Consistent command structure. Every action produces helpful, clear feedback.
- **History**: Optional lightweight log of interactions/events to reinforce continuity.

## Technical Guidelines
- **Persistence**: File-based, with JSON for data.
- **Dates & Time**: Standard Python libraries (`datetime`) for accurate age tracking.
- **Portability**: No exotic dependencies; pure Python preferred.
- **Scalability**: Supports many pets over time without performance loss.

---

This specification defines the foundation for TextPet: a minimal, efficient, positive, and hackable command-line virtual pet system.
