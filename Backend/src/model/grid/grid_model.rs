use crate::model::{cow::cow_structure::Cow, grid::grid_structure::Grid};

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
        let cells: Vec<Vec<Vec<_>>> = vec![vec![vec![]; cols as usize]; rows as usize];
        Grid {
            rows,
            cols,
            canvas_width: 500.0,
            canvas_height: 500.0,
            special_row: rows / 2,
            special_col: cols - 1,
            cells,
        }
    }

    pub fn add_cow(&mut self, cow: Cow) {
        self.cells[cow.y as usize][cow.x as usize].push(cow);
    }
}
