def simulate_tick(cows, grid, nb_tour, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, breeder_salary_evolution):
    for cow in cows:
        cow.act(grid, nb_tour, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, breeder_salary_evolution)
        if not cow.alive:
            print(f"Cow {cow.id} has died.")
            cows.remove(cow)
        
    # Vérifier s'il n'y a plus de vaches
    if not cows:
        print(f"Modèle achevé en {nb_tour} tours")
        exit()
    
    # Met à jour les couleurs des cases
    for row in grid:
        for box in row:
            box.update_color()
