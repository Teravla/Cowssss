use crate::enums::cell_role::Role;

#[derive(Clone)]
pub struct Cell {
    pub x: i32,
    pub y: i32,
    pub role: Role,
    pub passable: bool,
}
