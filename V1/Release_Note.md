# Release Notes – Version 1.0

## Cowssss – Simulation of Cow Needs in a Controlled Environment

### Overview

Version 1.0 of **Cowssss** introduces a simulation environment designed to model the needs and behaviors of cows within a controlled farm setting. This release provides a foundation for experimenting with AI-driven strategies to optimize farm productivity and revenue generation.

The simulation models cow behavior with respect to hunger, thirst, and milk production while allowing the player or AI to manage the farm efficiently.

---

### New Features

#### Field Environment

- **Grass patches (green tiles):** Source of food for cows.
- **Water sources (blue tiles):** Cows can drink to satisfy thirst.
- **Farm (grey tile):** Location for milking cows.

The environment is designed to simulate real-time resource consumption and movement within the farm.

#### Cow Attributes and Behavior

- **Hunger meter:** Decreases by 10% every tick.
- **Thirst meter:** Decreases by 10% every tick.
- **Milk production meter:** Increases by 5% per tick if hunger > 80% and thirst > 90%.

**Behavior rules per tick:**

1. Move one tile toward water if thirst < 50%.
2. Move one tile toward the nearest grass patch if hunger < 50%.
3. Die if basic needs are unmet.

**Milking behavior:**

- Cows move to the farm to be milked based on milk fullness:

  - > 90% milk: move 1 tile every 5 ticks
  - 80% milk: move 1 tile every 4 ticks
  - 60% milk: move 1 tile every 3 ticks
  - 40% milk: move 1 tile every 2 ticks
  - <20% milk: move 1 tile every tick
- After three milkings, cows die from exhaustion.

---

### Simulation Mechanics

- The system supports multiple cows and real-time tracking of their hunger, thirst, and milk production.
- Adaptive cow movement and placement logic are implemented to reflect realistic behavior within the environment.
- Multi-threading and responsive updates ensure smooth simulation of multiple entities simultaneously.
- Graphical output supports visualization of farm status, cow positions, and milk production trends.

---

### AI Integration

- Initial framework for AI strategies to optimize cow milking schedules and farm revenue.
- Supports reflection on neural network choices and experimentation with multiple parameters for decision-making.

---

### Improvements and Fixes

- Optimized field regeneration and food recovery mechanics.
- Cleaned Git cache and implemented proper `.gitignore` rules.
- Enhanced model logic for realistic cow behavior and prioritization of needs.
- Global improvements to codebase structure and maintainability.

---

### Future Roadmap

- Implementation of more sophisticated AI strategies for farm management.
- Extended environmental events (weather, dynamic water availability).
- Enhanced visualization and interactive simulation dashboard.

---

**Repository Commits Included in This Release:**

- Multiple simulation enhancements
- Reflection on neural network choices
- Adaptive cow placement and movement
- Multi-threading support
- Field regeneration and food recovery
- Farmer revenue based on cow feeding
- Graph display and data analysis
- Core simulation mechanics

---

This release provides a fully functional foundation for simulating cow needs and farm management while enabling AI-driven optimization of farm productivity.
