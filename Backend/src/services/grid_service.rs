use crate::model::grid::grid_structure::Grid;
use web_sys::CanvasRenderingContext2d;

pub fn draw_grid(ctx: &CanvasRenderingContext2d, grid: &Grid) {
    for row in &grid.cells {
        for cell in row {
            ctx.set_fill_style_str(cell.color());
            ctx.fill_rect(
                cell.x as f64 * grid.cell_width(),
                cell.y as f64 * grid.cell_height(),
                grid.cell_width(),
                grid.cell_height(),
            );
        }
    }

    // Tracer les lignes horizontales
    for i in 0..=grid.rows {
        ctx.begin_path();
        ctx.move_to(0.0, i as f64 * grid.cell_height());
        ctx.line_to(
            grid.cell_width() * (grid.cols - 1) as f64,
            i as f64 * grid.cell_height(),
        );
        ctx.stroke();
    }

    // Tracer les lignes verticales
    for j in 0..=grid.cols {
        if j == grid.special_col + 1 {
            continue;
        }
        ctx.begin_path();
        ctx.move_to(j as f64 * grid.cell_width(), 0.0);
        ctx.line_to(j as f64 * grid.cell_width(), grid.canvas_height);
        ctx.stroke();
    }
}
