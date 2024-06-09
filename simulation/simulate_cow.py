def simulate_tick(cows, grid):
    for cow in cows:
        cow.act(grid)
        if not cow.alive:
            print(f"Cow {cow.id} has died.")
            cows.remove(cow)
