use std::collections::HashMap;

#[derive(Clone)]
pub struct Cow {
    pub id: usize,
    pub x: i32,
    pub y: i32,
    pub radius: f64,
    pub color: String,
    pub dim_box: i32,
    pub tick_count: u32,
    pub path_to_farm: Vec<(i32, i32)>,
    pub spacing: i32,
    pub nb_square: i32,
    pub color_visit_count: HashMap<String, u32>,

    // Besoins
    pub hunger: i32,
    pub thirst: i32,
    pub milk: i32,
    pub alive: bool,
    pub number_milking: u32,
    pub reason_death: Option<String>,
}
