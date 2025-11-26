use std::collections::{BinaryHeap, HashMap};

#[derive(Eq, PartialEq)]
struct DijkstraNode {
    position: (i32, i32),
    cost: u32,
}

impl Ord for DijkstraNode {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        // min-heap : inverse order
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for DijkstraNode {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

pub fn dijkstra_pathfinding(
    grid: &crate::model::grid::grid_structure::Grid,
    start: (i32, i32),
    goal: (i32, i32),
) -> Option<Vec<(i32, i32)>> {
    let mut open_set: BinaryHeap<DijkstraNode> = BinaryHeap::new();
    let mut came_from: HashMap<(i32, i32), (i32, i32)> = HashMap::new();
    let mut cost_so_far: HashMap<(i32, i32), u32> = HashMap::new();

    cost_so_far.insert(start, 0);
    open_set.push(DijkstraNode {
        position: start,
        cost: 0,
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
            let cell: &crate::model::cell::cell_structure::Cell =
                &grid.cells[ny as usize][nx as usize];
            if !cell.passable {
                continue;
            }

            let new_cost: u32 = cost_so_far[&current.position] + 1;
            if new_cost < *cost_so_far.get(&(nx, ny)).unwrap_or(&u32::MAX) {
                cost_so_far.insert((nx, ny), new_cost);
                came_from.insert((nx, ny), current.position);
                open_set.push(DijkstraNode {
                    position: (nx, ny),
                    cost: new_cost,
                });
            }
        }
    }

    None
}
