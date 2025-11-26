use crate::{enums::cell_role::Role, model::cell::cell_structure::Cell};

impl Cell {
    pub fn new(x: i32, y: i32, role: Role) -> Self {
        let (passable, max_capacity, recovery_ticks) = match role {
            Role::Water => (false, u32::MAX, 0),
            Role::Hay => (true, 5, 3),
            Role::Grass => (true, 20, 10),
            Role::Farm => (true, 0, 0),
        };

        Cell {
            x,
            y,
            role,
            passable,
            usable: true,
            max_capacity,
            current_capacity: max_capacity,
            recovery_ticks,
            current_recovery: 0,
        }
    }

    pub fn color(&self) -> &str {
        match self.role {
            Role::Water => "blue",
            Role::Hay => "yellow",
            Role::Grass => "green",
            Role::Farm => "black",
        }
    }

    /// Use the cell by a cow
    /// Returns `true` if the use is possible
    pub fn use_cell(&mut self) -> bool {
        if !self.usable {
            return false;
        }

        if self.max_capacity != u32::MAX {
            // decrease the capacity
            if self.current_capacity > 0 {
                self.current_capacity -= 1;
            }

            if self.current_capacity == 0 {
                // cell exhausted, start recovery
                self.usable = false;
                self.current_recovery = self.recovery_ticks;
            }
        }

        true
    }

    /// Tick: decrements the recovery counter and reactivates the cell if possible
    pub fn tick(&mut self) {
        if self.current_recovery > 0 {
            self.current_recovery -= 1;
            if self.current_recovery == 0 {
                self.usable = true;
                self.current_capacity = self.max_capacity;
            }
        }
    }
}
