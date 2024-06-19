import random
import tkinter as tk
from typing import List, Tuple
from simulation.algorithm.algorithms import Algorithm

class Cow:
    """
    This class represents a cow in the simulation.
    """

    # Variable statique pour attribuer un identifiant unique à chaque vache
    cow_id_counter = 0

    def __init__(self, canvas: tk.Canvas, x: int, y:int , radius: float, color: str, dim_box: int, init_thirst: int, init_hunger: int, init_milk: int, farm: 'Farm', spacing: int):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius // 1.25
        self.color = color
        self.dim_box = dim_box
        self.tick_count = 0
        self.path_to_farm = []
        self.spacing = spacing

        self.color_visit_count = {
            "green": 0,
            "yellow": 0,
            "brown": 0,
            "orange": 0,
            "lightgray": 0,
            "blue": 0,
        }

        # Attributs des besoins de la vache
        self.hunger = init_hunger  # Jauge de faim (0-100)
        self.thirst = init_thirst  # Jauge de soif (0-100)
        self.milk = init_milk  # Jauge de capacité laitière (0-100)
        self.alive = True  # État de vie de la vache
        self.number_milking = 0  # Nombre de fois que la vache a été traitée
        self.reason_death = None  # Raison de la mort de la vache

        # Attributs de l'identifiant de la vache
        self.id = Cow.cow_id_counter
        Cow.cow_id_counter += 1

        self.farm = farm  # Référence à l'instance de la ferme
        self.algo = Algorithm()

        self.draw(self.radius, self.color, self.dim_box)

    def get_breeder_salary(self) -> float:
        """
        This method is used to get the breeder salary of the farm.
        """
        print(f"Le salaire de l'éleveur pour la vache {self.id} est de {self.farm.breeder_salary} dans cows.py.")
        return self.farm.breeder_salary


    def draw(self, radius: float, color: str, dim_box: int) -> None:
            """
            This method is used to draw a cow on the canvas.
            """

            center_x = self.x * (dim_box + self.spacing) + dim_box
            center_y = self.y * (dim_box + self.spacing) + dim_box
            self.circle_id = self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=color)


    def update_needs(self, hunger_evolution: int, thirst_evolution: int, milk_evolution: int, hunger_to_milk: int, thirst_to_milk: int) -> None:
        """
        This method is used to update the needs of the cow.
        """
        
        # Mise à jour des besoins de la vache
        if self.thirst > 0 and self.hunger > 0:
            self.thirst -= thirst_evolution
            self.hunger -= hunger_evolution

        # Vache meurt si ses jauges sont à 0
        if self.hunger <= 0 or self.thirst <= 0:
            self.alive = False
            self.reason_death = "hunger" if self.hunger <= 0 else "thirst"
        
        if self.alive and self.hunger >= hunger_to_milk and self.thirst >= thirst_to_milk:
            self.milk += milk_evolution


    def find_nearest(self, grid: List, target_colors: List[str]) -> tuple[int, int] | None:
        """
        This method is used to find the nearest position of a specific color.
        """
        
        if not target_colors:
            return None
        
        chosen_color = random.choice(target_colors)
        
        min_distance = float('inf')
        nearest_position = None

        for dx in range(-len(grid), len(grid)):
            for dy in range(-len(grid[0]), len(grid[0])):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                    if grid[new_x][new_y].color == chosen_color:
                        distance = abs(dx) + abs(dy)
                        if distance < min_distance:
                            min_distance = distance
                            nearest_position = (new_x, new_y)
        
        return nearest_position


    def move(self, dx: int, dy: int, grid: List, cows: List['Cow']) -> None:
        """
        This method is used to move the cow on the grid.
        """
        
        if self.alive:
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Vérifie si la nouvelle position n'est pas une case bleue
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y].color != "blue":
                # Vérifie si la nouvelle position n'est pas déjà occupée par une autre vache
                if not any(cow.x == new_x and cow.y == new_y for cow in cows if cow.alive and cow != self):
                    self.x = new_x
                    self.y = new_y
                    self.canvas.move(self.circle_id, dx * 30, dy * 30)  # Déplacer le cercle correspondant à la vache
            else:
                print(f"Vache {self.id} ne peut pas se déplacer sur la case bleue.")
                print(f"La case bleue est à la position ({new_x}, {new_y}) et la vache est à la position ({self.x}, {self.y}).")
                exit()


    def go_to_farm(self, grid: List, algorithm: str, mix_food_params: dict[str, dict[str, str | int | float]]) -> None:
        """
        This method is used to move the cow to the farm.
        """
        
        if self.alive:
            if not self.path_to_farm:  # Calcule le chemin seulement si nécessaire
                if algorithm == 'astar':
                    self.path_to_farm = self.algo.astar_pathfinding((self.x, self.y), (0, len(grid[0]) // 2), grid)
                elif algorithm == 'dijkstra':
                    self.path_to_farm = self.algo.dijkstra_pathfinding((self.x, self.y), (0, len(grid[0]) // 2), grid)
                else:
                    raise ValueError("Unknown algorithm specified.")

            if self.path_to_farm:
                next_step = self.path_to_farm.pop(0)  # Prend la prochaine étape du chemin
                dx = next_step[0] - self.x
                dy = next_step[1] - self.y
                self.move(dx, dy, grid, self.farm.cows)
                if not self.alive:
                    return

                if self.x == 0 and self.y == len(grid[0]) // 2:
                    # Correspondance couleur-nourriture
                    color_to_food = {v['color']: k for k, v in mix_food_params.items()}

                    # Trouver la qualité minimale parmi les couleurs visitées
                    min_quality = min(
                        mix_food_params[color_to_food[color]]['quality']
                        for color in self.color_visit_count if color in color_to_food
                    )

                    total_result = 0
                    visited_colors_count = -1

                    for color, count in self.color_visit_count.items():
                        if color in color_to_food:
                            food_type = color_to_food[color]
                            milk_value = mix_food_params[food_type]["milk_value"]
                            # Calculer le résultat
                            result = int(count) * float(milk_value) * float(min_quality)
                            total_result += result
                            visited_colors_count += 1

                    # Calculer le résultat moyen
                    if visited_colors_count > 0:
                        average_result = total_result / visited_colors_count
                    else:
                        average_result = 0

                    # Calculer le salaire pour cette vache
                    cow_salary = average_result * 100

                    self.number_milking += 1
                    self.farm.breeder_salary += cow_salary
                    self.milk = 0
                    self.hunger = 20
                    self.thirst = 20
                    self.path_to_farm = []  # Réinitialise le chemin après l'arrivée


    def act(self, grid: List, hunger_evolution: int, thirst_evolution: int, milk_evolution: int, add_hunger: int, add_thirst: int, hunger_to_milk: int, thirst_to_milk: int, algorithm_to_farm: str, mix_food_params: dict[str, dict[str, str | int | float]]) -> None:
        """
        This method is used to simulate the cow's actions. It's the main method of the Cow class.
        """

        self.tick_count += 1

        if self.number_milking >= 1:
            self.alive = False
            self.reason_death = "milking"
            return

        needs_updated = False  # Variable pour suivre si les besoins ont été mis à jour

        food_colors_nb: List[str] = [food["color"] for food in mix_food_params.values() if isinstance(food["color"], str) and food["color"] != "blue"]

        if self.alive and (0 <= self.x < len(grid) and 0 <= self.y < len(grid[0])):

            if self.milk >= 100:
                self.go_to_farm(grid, algorithm_to_farm, mix_food_params)
                return  # Sortie anticipée si la vache est en train de traire
            
            # Si la vache a soif, chercher la case la plus proche de couleur "blue"
            if self.thirst < thirst_to_milk:
                target = self.find_nearest(grid, ["blue"])
                if target:
                    self.move_towards(target, grid)
                    self.drink(grid, add_thirst)
                    needs_updated = True
            
            # Sinon, si la vache a faim, chercher la case la plus proche d'une couleur de nourriture
            elif self.hunger < hunger_to_milk:
                target = self.find_nearest(grid, food_colors_nb)
                if target:
                    self.move_towards(target, grid)
                    self.eating(grid, add_hunger)
                    needs_updated = True
            
            # Si la vache n'a pas besoin de se déplacer, indiquer que les besoins ont été mis à jour
            else:
                needs_updated = True

        if needs_updated:
            self.update_needs(hunger_evolution, thirst_evolution, milk_evolution, hunger_to_milk, thirst_to_milk)
        

    def recover(self, grid: List, mix_food_params: dict[str, dict[str, str | int | float]], color: str) -> None:
        """
        This method is used to recover the cow.
        """

        # Met à jour les couleurs des cases
        for row in grid:
            for box in row:
                box.update_color()
                if box.time_to_recovery == 0 and box.color == "black":
                    
                    choice_color = color
                    
                    # Chercher les paramètres associés à la couleur choisie
                    for food_type, params in mix_food_params.items():
                        if params["color"] == choice_color:
                            food_value = float(params["food_value"])
                            food_lifetime = float(params["food_lifetime"])

                            
                            # Réduire le salaire de l'éleveur par food_value de la couleur choisie
                            if self.farm.breeder_salary >= food_value:
                                self.farm.breeder_salary -= food_value
                                box.recolor(choice_color, food_lifetime)
                            break  # Sortir de la boucle une fois que nous avons trouvé et traité la couleur choisie


    def move_towards(self, target: Tuple[int, int], grid: List) -> None:
        """
        This method is used to move the cow towards a target.
        """
        
        if target:
            target_x, target_y = target
            dx = 1 if target_x > self.x else -1 if target_x < self.x else 0
            dy = 1 if target_y > self.y else -1 if target_y < self.y else 0

            # Vérifie les mouvements possibles sans se déplacer vers une case bleue
            if 0 <= self.x + dx < len(grid) and 0 <= self.y + dy < len(grid[0]) and grid[self.x + dx][self.y + dy].color != "blue":
                self.move(dx, dy, grid, self.farm.cows)
            elif dx != 0 and 0 <= self.x + dx < len(grid) and grid[self.x + dx][self.y].color != "blue":
                self.move(dx, 0, grid, self.farm.cows)
            elif dy != 0 and 0 <= self.y + dy < len(grid[0]) and grid[self.x][self.y + dy].color != "blue":
                self.move(0, dy, grid, self.farm.cows)


    def drink(self, grid: List, add_thirst: int) -> None:
        """
        This method is used to simulate the cow drinking water.
        """
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue  # Ignore la case où la vache se trouve actuellement
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                    if grid[new_x][new_y].color == "blue":
                        # La vache boit de l'eau sans se déplacer sur la case bleue
                        self.thirst = add_thirst
                        return
                        

    def eating(self, grid: List, add_hunger: int) -> None:
        """
        This method is used to simulate the cow eating food.
        """
        
        current_box = grid[self.x][self.y]

        if current_box.color not in ["blue", "gray", "black"] and current_box.food_lifetime > 0:
            self.color_visit_count[current_box.color] += 1
            self.hunger += add_hunger
            self.hunger = min(self.hunger, 100)
            current_box.food_lifetime -= 1

            if current_box.food_lifetime == 0:
                current_box.set_color("black")
        return




class Farm:
    """
    This class represents a farm in the simulation.
    """
    
    def __init__(self, canvas: tk.Canvas, pre: List, nb_square: int, nb_cow: int, radius: float, color: str, dim_box: int, init_thirst: int, init_hunger: int, init_milk: int, init_salary: float, spacing: int):
        self.canvas = canvas
        self.pre = pre
        self.nb_square = nb_square
        self.breeder_salary = init_salary
        self.spacing = spacing
        self.cows = self.create_cows(nb_cow, radius, color, dim_box, init_thirst, init_hunger, init_milk, self.spacing)


    def create_cows(self, nb_cow: int, radius: float, color: str, dim_box: int, init_thirst: int, init_hunger: int, init_milk: int, spacing: int) -> List[Cow]:
        """
        This method is used to create cows in the farm.
        """
        
        coo_central_x = self.nb_square // 2 + 1 
        coo_central_y = self.nb_square // 2 + 1

        # Fonction pour vérifier si une position est valide pour placer une vache
        def is_valid_position(x, y):
            return (0 <= x < self.nb_square and 0 <= y < self.nb_square and
                    self.pre[x][y].color != "blue" and not self.pre[x][y].has_cow)

        # Liste pour stocker les instances de vache créées
        created_cows = []

        for i in range(nb_cow):
            x = coo_central_x
            y = coo_central_y

            # Recherche d'une case valide autour de la vache
            search_radius = 1
            placed = False
            while not placed:
                for dx in range(-search_radius, search_radius + 1):
                    for dy in range(-search_radius, search_radius + 1):
                        new_x, new_y = x + dx, y + dy
                        if is_valid_position(new_x, new_y):
                            x, y = new_x, new_y
                            cow = Cow(self.canvas, x, y, radius, color, dim_box, init_thirst, init_hunger, init_milk, self, spacing)

                            self.pre[x][y].has_cow = True
                            created_cows.append(cow)  # Ajout de la vache créée à la liste
                            placed = True
                            break
                    if placed:
                        break
                search_radius += 1
                if search_radius > self.nb_square:
                    break

            if not placed:
                print("Aucune position valide n'a été trouvée pour la vache.")

        return created_cows  # Retourner la liste des vaches créées
