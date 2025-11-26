use std::cell::RefCell;

use crate::services::cow_service::draw_cow;
use crate::services::game_service::tick;
use crate::{model::cow::cow_structure::Cow, services::grid_service::draw_grid};
use wasm_bindgen::{JsCast, JsValue, prelude::wasm_bindgen};
use web_sys::CanvasRenderingContext2d;

use crate::model::grid::grid_structure::Grid;

pub mod enums {
    pub mod cell_role;
    pub mod cow_action;
}

pub mod core {
    pub mod astar_pathfinding;
    pub mod dijkstra_pathfinding;
}

pub mod model {
    pub mod grid {
        pub mod grid_model;
        pub mod grid_structure;
    }
    pub mod cow {
        pub mod cow_model;
        pub mod cow_structure;
    }
    pub mod cell {
        pub mod cell_model;
        pub mod cell_structure;
    }
}

pub mod services {
    pub mod cow_service;
    pub mod game_service;
    pub mod grid_service;
}

// instance globale mutable sécurisée
thread_local! {
    static GRID: RefCell<Option<Grid>> = RefCell::new(None);
}

#[wasm_bindgen]
pub fn render(ctx: &JsValue, number_of_cows: usize) {
    let ctx: CanvasRenderingContext2d = ctx
        .clone()
        .dyn_into()
        .expect("Impossible de convertir en CanvasRenderingContext2d");

    GRID.with(|cell: &RefCell<Option<Grid>>| {
        let mut cell: std::cell::RefMut<'_, Option<Grid>> = cell.borrow_mut();
        let grid: &mut Grid = cell.get_or_insert_with(Grid::new);

        // Création des vaches si aucune
        let total_cows: usize = grid
            .cows
            .iter()
            .flat_map(|r: &Vec<Vec<Cow>>| r.iter())
            .map(|v: &Vec<Cow>| v.len())
            .sum();
        if total_cows == 0 {
            let black_x = grid.special_col;
            let black_y = grid.special_row;
            for _ in 0..number_of_cows {
                let cow = Cow::new(
                    black_x,
                    black_y,
                    15.0,
                    "brown".into(),
                    50,
                    50,
                    50,
                    50,
                    0,
                    12,
                );
                grid.add_cow(cow);
            }
        }

        draw_grid(&ctx, grid);
        for row in 0..grid.rows as usize {
            for col in 0..grid.cols as usize {
                for cow in &grid.cows[row][col] {
                    draw_cow(&ctx, cow, grid);
                }
            }
        }
    });
}

#[wasm_bindgen]
pub fn tick_js() {
    GRID.with(|cell: &RefCell<Option<Grid>>| {
        if let Some(grid) = cell.borrow_mut().as_mut() {
            tick(grid);

            let positions: Vec<_> = grid
                .cows
                .iter()
                .flat_map(|row: &Vec<Vec<Cow>>| row.iter())
                .flat_map(|col: &Vec<Cow>| col.iter())
                .map(|cow: &Cow| format!("({}, {})", cow.x, cow.y))
                .collect();
            web_sys::console::log_1(&format!("Cow positions: {:?}", positions).into());
        }
    });
}
