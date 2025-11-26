use crate::{enums::cow_action::CowAction, model::grid::grid_structure::Grid};

pub fn tick(grid: &mut Grid) {
    // 1️⃣ Collecter toutes les décisions des vaches
    let mut decisions: Vec<(usize, usize, usize, CowAction)> = vec![];
    for y in 0..grid.rows as usize {
        for x in 0..grid.cols as usize {
            // Cloner les vaches pour éviter de garder un emprunt mutable/immuable en même temps
            let cows_snapshot: Vec<_> = grid.cows[y][x].iter().cloned().collect();
            for (i, cow) in cows_snapshot.iter().enumerate() {
                if !cow.alive {
                    continue;
                }
                let action = cow.decide(&grid); // immuable
                decisions.push((y, x, i, action));
            }
        }
    }

    // 2️⃣ Exécuter les actions avec emprunt mutable
    for (y, x, i, action) in decisions.into_iter().rev() {
        match action {
            CowAction::Drink => {
                if let Some(cow) = grid.cows[y][x].get_mut(i) {
                    cow.drink(&grid.cells, 100);
                }
            }
            CowAction::Eat => {
                if let Some(cow) = grid.cows[y][x].get_mut(i) {
                    cow.eat(&mut grid.cells, 100);
                }
            }
            CowAction::Move((nx, ny)) => {
                let mut cow = grid.cows[y][x].remove(i);
                cow.x = nx;
                cow.y = ny;
                grid.cows[ny as usize][nx as usize].push(cow);
            }
            CowAction::Rest => {
                if let Some(cow) = grid.cows[y][x].get_mut(i) {
                    cow.tick_count += 1;
                    if cow.hunger > 0 {
                        cow.hunger -= 1;
                    }
                    if cow.thirst > 0 {
                        cow.thirst -= 1;
                    }
                    if cow.hunger >= 50 && cow.thirst >= 50 {
                        cow.milk += 1;
                    }
                }
            }
        }
    }

    // 3️⃣ Mettre à jour les cellules
    for row in grid.cells.iter_mut() {
        for cell in row.iter_mut() {
            cell.tick();
        }
    }
}
