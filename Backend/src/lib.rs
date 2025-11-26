use crate::services::cow_service::draw_cow;
use crate::{model::cow::cow_structure::Cow, services::grid_service::draw_grid};
use wasm_bindgen::{JsCast, JsValue, prelude::wasm_bindgen};
use web_sys::CanvasRenderingContext2d;

use crate::model::grid::grid_structure::Grid;

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
    pub mod grid_service;
}

pub mod enums {
    pub mod cell_role;
}

#[wasm_bindgen]
pub fn render(ctx: &JsValue, number_of_cows: usize) {
    let ctx: CanvasRenderingContext2d = ctx
        .clone()
        .dyn_into()
        .expect("Impossible de convertir en CanvasRenderingContext2d");

    let mut grid: Grid = Grid::new();
    draw_grid(&ctx, &grid);

    // Position de la case noire
    let black_x = grid.special_col;
    let black_y = grid.special_row;

    // Créer les vaches et les dessiner
    for _i in 0..number_of_cows {
        let cow = Cow::new(
            black_x,
            black_y,        // toutes sur la case noire
            15.0,           // radius
            "brown".into(), // couleur
            50,             // dim_box (optionnel)
            50,
            50,
            50, // thirst, hunger, milk
            0,  // spacing
            12, // nb_square
        );

        grid.add_cow(cow);
    }

    for row in 0..grid.rows as usize {
        for col in 0..grid.cols as usize {
            for cow in &grid.cows[row][col] {
                draw_cow(&ctx, cow, &grid);
            }
        }
    }
}
