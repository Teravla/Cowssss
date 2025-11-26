use crate::model::{cow::cow_structure::Cow, grid::grid_structure::Grid};
use std::collections::HashMap;

impl Cow {
    pub fn new(
        x: i32,
        y: i32,
        radius: f64,
        color: String,
        dim_box: i32,
        init_thirst: i32,
        init_hunger: i32,
        init_milk: i32,
        spacing: i32,
        nb_square: i32,
    ) -> Self {
        let mut color_visit_count: HashMap<String, u32> = HashMap::new();
        color_visit_count.insert("green".to_string(), 0);
        color_visit_count.insert("yellow".to_string(), 0);
        color_visit_count.insert("brown".to_string(), 0);
        color_visit_count.insert("orange".to_string(), 0);
        color_visit_count.insert("lightgray".to_string(), 0);
        color_visit_count.insert("blue".to_string(), 0);

        static mut COW_ID_COUNTER: usize = 0;
        let id: usize;
        unsafe {
            id = COW_ID_COUNTER;
            COW_ID_COUNTER += 1;
        }

        Cow {
            id,
            x,
            y,
            radius: radius / 1.5,
            color,
            dim_box,
            tick_count: 0,
            path_to_farm: vec![],
            spacing,
            nb_square,
            color_visit_count,
            hunger: init_hunger,
            thirst: init_thirst,
            milk: init_milk,
            alive: true,
            number_milking: 0,
            reason_death: None,
        }
    }

    pub fn drink(&mut self, grid: &Grid, add_thirst: i32) {
        let directions: [(i32, i32); 8] = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ];

        for (dx, dy) in directions {
            let new_x: i32 = self.x + dx;
            let new_y: i32 = self.y + dy;

            if let Some(cell) = grid.cell_at(new_x, new_y) {
                if cell.role == crate::enums::cell_role::Role::Water {
                    // Cow drinks without moving
                    self.thirst = add_thirst;
                    return;
                }
            }
        }
    }

    pub fn eat(&mut self, grid: &mut Grid, add_hunger: i32) {
        if let Some(cell) = grid.cell_at_mut(self.x, self.y) {
            match cell.role {
                crate::enums::cell_role::Role::Hay | crate::enums::cell_role::Role::Grass => {
                    self.hunger += add_hunger;
                    if self.hunger > 100 {
                        self.hunger = 100;
                    }
                    cell.use_cell();
                }
                _ => {} // Water or Farm cells cannot be eaten from
            }
        }
    }
}
