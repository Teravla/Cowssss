pub enum CowAction {
    Eat,
    Drink,
    Move((i32, i32)), // move to new (x, y) position
    Rest,
}
