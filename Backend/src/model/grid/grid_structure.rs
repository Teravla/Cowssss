use crate::model::cow::cow_structure::Cow;

pub struct Grid {
    pub rows: i32,
    pub cols: i32,
    pub canvas_width: f64,
    pub canvas_height: f64,
    pub special_row: i32,
    pub special_col: i32,

    // 2D vector to hold cows in each cell
    pub cells: Vec<Vec<Vec<Cow>>>,
}
