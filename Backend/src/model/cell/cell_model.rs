use crate::{enums::cell_role::Role, model::cell::cell_structure::Cell};

impl Cell {
    pub fn new(x: i32, y: i32, role: Role) -> Self {
        let passable = match role {
            Role::Water => false,
            Role::Hay | Role::Grass => true,
            Role::Black => false,
        };
        Cell { x, y, role, passable }
    }

    pub fn color(&self) -> &str {
        match self.role {
            Role::Water => "blue",
            Role::Hay => "yellow",
            Role::Grass => "green",
            Role::Black => "black",
        }
    }
}