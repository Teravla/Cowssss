use std::collections::{BinaryHeap, HashMap};

#[derive(Eq, PartialEq)]
struct Node {
    position: (i32, i32),
    cost: u32,     // cost from start to this node
    estimate: u32, // cost + heuristic
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        // min-heap : inverse order
        other
            .estimate
            .cmp(&self.estimate)
            .then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

// Manhattan distance comme u32
fn heuristic(a: (i32, i32), b: (i32, i32)) -> u32 {
    ((a.0 - b.0).abs() + (a.1 - b.1).abs()) as u32
}

pub fn astar_pathfinding(
    grid: &crate::model::grid::grid_structure::Grid,
    start: (i32, i32),
    goal: (i32, i32),
) -> Option<Vec<(i32, i32)>> {
    let mut open_set = BinaryHeap::new();
    let mut came_from: HashMap<(i32, i32), (i32, i32)> = HashMap::new();
    let mut g_score: HashMap<(i32, i32), u32> = HashMap::new();

    g_score.insert(start, 0);
    open_set.push(Node {
        position: start,
        cost: 0,
        estimate: heuristic(start, goal),
    });

    while let Some(current) = open_set.pop() {
        if current.position == goal {
            // reconstruct the path
            let mut path: Vec<(i32, i32)> = vec![goal];
            let mut current_pos: (i32, i32) = goal;
            while let Some(&prev) = came_from.get(&current_pos) {
                path.push(prev);
                current_pos = prev;
            }
            path.reverse();
            return Some(path);
        }

        let (x, y) = current.position;
        let neighbors: [(i32, i32); 4] = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)];

        for &(nx, ny) in &neighbors {
            if nx < 0 || ny < 0 || nx >= grid.cols || ny >= grid.rows {
                continue;
            }
            let cell: &crate::model::cell::cell_structure::Cell = &grid.cells[ny as usize][nx as usize];
            if !cell.passable {
                continue;
            }

            let tentative_g: u32 = g_score[&current.position] + 1; // uniform cost
            if tentative_g < *g_score.get(&(nx, ny)).unwrap_or(&u32::MAX) {
                came_from.insert((nx, ny), current.position);
                g_score.insert((nx, ny), tentative_g);
                let f: u32 = tentative_g + heuristic((nx, ny), goal);
                open_set.push(Node {
                    position: (nx, ny),
                    cost: tentative_g,
                    estimate: f,
                });
            }
        }
    }

    None
}
