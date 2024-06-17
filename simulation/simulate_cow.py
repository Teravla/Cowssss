from data.result import append_to_csv

def simulate_tick(cows, grid, nb_tour, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, breeder_salary_evolution, percentage_hunger, percentage_thirst, algorithm_to_farm, csv_filepath, show_analysis, mix_food_params):
    all_cows_data = []

    for cow in cows:
        cow.act(grid, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, breeder_salary_evolution, percentage_hunger, percentage_thirst, algorithm_to_farm, mix_food_params)
        if not cow.alive:
            print(f"Cow {cow.id} has died by {cow.reason_death}.")
            cows.remove(cow)
        
        cow_data = {
            cow.id: {
                'x': cow.x,
                'y': cow.y,
                'hunger': cow.hunger,
                'thirst': cow.thirst,
                'milk': cow.milk
            }
        }
        all_cows_data.append(cow_data)

    # Met à jour les couleurs des cases
    for row in grid:
        for box in row:
            box.update_color()

    if show_analysis:
        append_to_csv(csv_filepath, all_cows_data, nb_tour)


