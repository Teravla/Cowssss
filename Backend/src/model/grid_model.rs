use js_sys::Math;
use wasm_bindgen::JsCast;
use wasm_bindgen::prelude::*;
use web_sys::CanvasRenderingContext2d;

#[wasm_bindgen]
pub fn draw_grid(ctx: &JsValue) {
    let ctx: CanvasRenderingContext2d = ctx
        .clone()
        .dyn_into()
        .expect("Impossible de convertir en CanvasRenderingContext2d");

    let rows: i32 = 11;
    let cols: i32 = 12;
    let canvas_width: f64 = 500.0;
    let canvas_height: f64 = 500.0;
    let cell_width: f64 = canvas_width / cols as f64;
    let cell_height: f64 = canvas_height / rows as f64;

    let special_col = 11; // 12ème colonne (0-indexed)
    let special_row = 5; // ligne du milieu (0-indexed)

    // Remplissage aléatoire
    for i in 0..rows {
        for j in 0..cols {
            if i == special_row && j == special_col {
                // Case noire forcée
                ctx.set_fill_style_str("black");
            } else if j != special_col {
                // Couleurs aléatoires uniquement si ce n'est pas la colonne spéciale
                let r = Math::random();
                if r < 0.05 {
                    ctx.set_fill_style_str("blue");
                } else if r < 0.2 {
                    ctx.set_fill_style_str("yellow");
                } else {
                    ctx.set_fill_style_str("green");
                }
            } else {
                // Colonne spéciale (j == special_col) et pas la ligne spéciale → transparent
                ctx.set_fill_style_str("white"); // ou ne pas remplir
            }

            ctx.fill_rect(
                j as f64 * cell_width,
                i as f64 * cell_height,
                cell_width,
                cell_height,
            );
        }
    }

    // Tracer les lignes
    // Lignes horizontales
    for i in 0..=rows {
        ctx.begin_path();
        ctx.move_to(0.0, i as f64 * cell_height);
        ctx.line_to(cell_width * (cols - 1) as f64, i as f64 * cell_height);
        ctx.stroke();
    }
    // Lignes verticales
    for j in 0..=cols {
        if j == special_col + 1 {
            continue; // on saute la 12ᵉ colonne (bordure droite de la colonne spéciale)
        }
        ctx.begin_path();
        ctx.move_to(j as f64 * cell_width, 0.0);
        ctx.line_to(j as f64 * cell_width, canvas_height);
        ctx.stroke();
    }
}
