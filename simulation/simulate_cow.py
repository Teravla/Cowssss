from typing import List, Tuple, Dict, Optional, Union
from data.result import append_to_csv
from simulation.cow import Cow

def simulate_tick(
    cows: List[Cow], grid: List, nb_tour: int, hunger_evolution: int, thirst_evolution: int, milk_evolution: int, add_hunger: int, add_thirst: int,
    percentage_hunger: int, percentage_thirst: int, algorithm_to_farm: str, csv_filepath: Optional[str], show_analysis: bool,
    mix_food_params: Dict[str, Dict[str, Union[str, int, float]]], breeder_salary: float,
    reason_death: List[str], cow_id: List[int]
) -> Tuple[float, List[str], List[int]]:
    """
    Simulate a tick of the simulation.
    """
    all_cows_data = []

    for cow in cows:
        cow.act(grid, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, percentage_hunger, percentage_thirst, algorithm_to_farm, mix_food_params)

        if not cow.alive:
            cows.remove(cow)
            if cow.reason_death is not None:
                reason_death.append(cow.reason_death)
            if cow.id is not None:
                cow_id.append(cow.id)

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

        if len(cows) != 0 and cow == cows[-1]:
            cow.recover(grid, mix_food_params)
            current_breeder_salary = cow.get_breeder_salary() if cow.get_breeder_salary() is not None else -2
            breeder_salary = max(breeder_salary, current_breeder_salary)

    if show_analysis:
        append_to_csv(csv_filepath, all_cows_data, nb_tour)
    
    return (breeder_salary, reason_death, cow_id)
