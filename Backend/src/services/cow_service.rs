use crate::model::cow::cow_structure::Cow;
use crate::model::grid::grid_structure::Grid;
use web_sys::CanvasRenderingContext2d;

pub fn draw_cow(ctx: &CanvasRenderingContext2d, cow: &Cow, grid: &Grid) {
    // Calcul de la position sur la grille
    let x: f64 = cow.x as f64 * grid.cell_width() + grid.cell_width() / 2.0;
    let y: f64 = cow.y as f64 * grid.cell_height() + grid.cell_height() / 2.0;

    ctx.begin_path();
    ctx.arc(x, y, cow.radius, 0.0, std::f64::consts::PI * 2.0)
        .expect("Impossible de créer l'arc pour la vache");
    ctx.set_fill_style_str(&cow.color);
    ctx.fill();
    ctx.stroke();
}
