use crate::{
    enums::cell_role::Role,
    model::{cell::cell_structure::Cell, cow::cow_structure::Cow, grid::grid_structure::Grid},
};

impl Grid {
    pub fn cell_width(&self) -> f64 {
        self.canvas_width / self.cols as f64
    }

    pub fn cell_height(&self) -> f64 {
        self.canvas_height / self.rows as f64
    }

    pub fn new() -> Self {
        let rows: i32 = 11;
        let cols: i32 = 12;
        let mut cells: Vec<Vec<Cell>> = vec![];
        let cows: Vec<Vec<Vec<Cow>>> = vec![vec![vec![]; cols as usize]; rows as usize];

        for i in 0..rows {
            let mut row_cells: Vec<Cell> = vec![];
            for j in 0..cols {
                let role = if j == cols - 1 {
                    if i == rows / 2 {
                        // case noire centrale
                        Role::Black
                    } else {
                        // aucune cellule pour les autres lignes de la dernière colonne
                        continue;
                    }
                } else {
                    let r: f64 = js_sys::Math::random();
                    if r < 0.05 {
                        Role::Water
                    } else if r < 0.2 {
                        Role::Hay
                    } else {
                        Role::Grass
                    }
                };
                row_cells.push(Cell::new(j, i, role));
            }
            cells.push(row_cells);
        }

        Grid {
            rows,
            cols,
            canvas_width: 500.0,
            canvas_height: 500.0,
            special_row: rows / 2,
            special_col: cols - 1,
            cells,
            cows,
        }
    }

    pub fn add_cow(&mut self, cow: Cow) {
        self.cows[cow.y as usize][cow.x as usize].push(cow);
    }
}
