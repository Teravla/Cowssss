use wasm_bindgen::prelude::*;
use wasm_bindgen::JsCast;
use web_sys::CanvasRenderingContext2d;

#[wasm_bindgen]
pub fn draw_grid(ctx: &JsValue) {
    let ctx: CanvasRenderingContext2d = ctx
        .dyn_into()
        .expect("Impossible de convertir en CanvasRenderingContext2d");

    ctx.set_stroke_style_str("#000000");

    let rows = 10;
    let size = 50.0;

    // lignes horizontales
    for i in 0..=rows {
        ctx.begin_path();
        ctx.move_to(0.0, i as f64 * size);
        ctx.line_to(rows as f64 * size, i as f64 * size);
        ctx.stroke();
    }

    // lignes verticales
    for j in 0..=rows {
        ctx.begin_path();
        ctx.move_to(j as f64 * size, 0.0);
        ctx.line_to(j as f64 * size, rows as f64 * size);
        ctx.stroke();
    }
}
