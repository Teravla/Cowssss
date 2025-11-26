use crate::core::astar_pathfinding::astar_pathfinding;
use crate::enums::cow_action::CowAction;
use crate::model::cell::cell_structure::Cell;
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

    pub fn drink(&mut self, cells: &Vec<Vec<Cell>>, add_thirst: i32) {
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
            let new_x = self.x + dx;
            let new_y = self.y + dy;

            if new_y >= 0
                && new_y < cells.len() as i32
                && new_x >= 0
                && new_x < cells[0].len() as i32
            {
                let cell: &Cell = &cells[new_y as usize][new_x as usize];
                if cell.role == crate::enums::cell_role::Role::Water {
                    self.thirst = add_thirst;
                    return;
                }
            }
        }
    }

    pub fn eat(&mut self, cells: &mut Vec<Vec<Cell>>, add_hunger: i32) {
        if self.y >= 0
            && self.y < cells.len() as i32
            && self.x >= 0
            && self.x < cells[0].len() as i32
        {
            let cell = &mut cells[self.y as usize][self.x as usize];
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

    pub fn decide(&self, grid: &Grid) -> CowAction {
        if self.thirst < 50 {
            CowAction::Drink
        } else if self.hunger < 50 {
            CowAction::Eat
        } else {
            CowAction::Move(self.propose_move(grid))
        }
    }

    pub fn propose_move(&self, grid: &Grid) -> (i32, i32) {
        let target: Option<(i32, i32)> = if self.thirst < 50 {
            grid.find_nearest(crate::enums::cell_role::Role::Water, self.x, self.y)
        } else if self.hunger < 50 {
            grid.find_nearest(crate::enums::cell_role::Role::Hay, self.x, self.y)
                .or_else(|| grid.find_nearest(crate::enums::cell_role::Role::Grass, self.x, self.y))
        } else {
            None
        };

        if let Some(goal) = target {
            if let Some(path) = astar_pathfinding(grid, (self.x, self.y), goal) {
                if path.len() > 1 {
                    return path[1];
                }
            }
        }

        (self.x, self.y)
    }
}
