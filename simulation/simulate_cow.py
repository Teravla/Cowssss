from typing import List
from data.result import append_to_csv
from simulation.cow import Cow


def simulate_tick(cows: List[Cow], grid: List, nb_tour: int, hunger_evolution: int, thirst_evolution: int, milk_evolution: int, add_hunger: int, add_thirst: int, percentage_hunger: int, percentage_thirst: int, algorithm_to_farm: str, csv_filepath: str | None, show_analysis: bool, mix_food_params: dict[str, dict[str, str | int | float]]) -> None:
    """
    Simulate a tick of the simulation.
    """

    all_cows_data = []
    breeder_salary = 0

    for cow in cows:
        cow.act(grid, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, percentage_hunger, percentage_thirst, algorithm_to_farm, mix_food_params)

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

        if len(cows) != 0:
            if cow == cows[-1]:
                cow.recover(grid, mix_food_params, "yellow")
        

    

    if show_analysis:
        append_to_csv(csv_filepath, all_cows_data, nb_tour)


