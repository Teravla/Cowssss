def simulate_tick(cows, grid, nb_tour):
    for cow in cows:
        cow.act(grid)
        if not cow.alive:
            print(f"Cow {cow.id} has died.")
            cows.remove(cow)
    
    # Met à jour les couleurs des cases
    for row in grid:
        for box in row:
            box.update_color()

    # Vérifie si toutes les vaches sont mortes
    if not cows:
        print(f"Modèle achevé en {nb_tour} tours.")
        exit()  # Quitte le programme
