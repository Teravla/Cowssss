use crate::enums::cell_role::Role;

#[derive(Clone)]
pub struct Cell {
    pub x: i32,
    pub y: i32,
    pub role: Role, // Role of the cell (Water, Hay, Grass, Farm)
    pub passable: bool, // Whether cows can walk on this cell
    pub usable: bool,   // Whether cows can use resources on this cell

    // Capacities for resources
    pub max_capacity: u32,      // number of usage before depletion
    pub current_capacity: u32,  // remaining capacity
    pub recovery_ticks: u32,    // ticks to recover
    pub current_recovery: u32,  // recovery counter
}
