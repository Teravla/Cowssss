import random
import tkinter as tk

from numpy import average
from simulation.algorithm.algorithms import Algorithm
class Cow:
    # Variable statique pour attribuer un identifiant unique à chaque vache
    cow_id_counter = 0

    def __init__(self, canvas, x, y, radius, color, dim_box, init_thirst, init_hunger, init_milk, farm, spacing):
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

    def draw(self, radius, color, dim_box):
            # Calcul des coordonnées du centre du cercle
            center_x = self.x * (dim_box + self.spacing) + dim_box
            center_y = self.y * (dim_box + self.spacing) + dim_box
            # Dessin du cercle noir avec l'identifiant de la vache comme étiquette
            self.circle_id = self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=color)


    def update_needs(self, hunger_evolution, thirst_evolution, milk_evolution, hunger_to_milk, thirst_to_milk):
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


    def find_nearest(self, grid, target_colors):
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

    def move(self, dx, dy, grid, cows):
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

    def go_to_farm(self, grid, breeder_salary_evolution, algorithm, mix_food_params):
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
                    print(self.color_visit_count)
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
                            result = count * milk_value * min_quality
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
                    self.farm.breeder_salary += breeder_salary_evolution
                    self.milk = 0
                    self.hunger = 20
                    self.thirst = 20
                    self.path_to_farm = []  # Réinitialise le chemin après l'arrivée





    def act(self, grid, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, breeder_salary_evolution, hunger_to_milk, thirst_to_milk, algorithm_to_farm, mix_food_params):

        self.tick_count += 1

        if self.number_milking >= 1:
            self.alive = False
            self.reason_death = "milking"
            return

        needs_updated = False  # Variable pour suivre si les besoins ont été mis à jour

        food_colors_nb = [food["color"] for food in mix_food_params.values() if food["color"] != "blue"]

        if self.alive and (0 <= self.x < len(grid) and 0 <= self.y < len(grid[0])):

            if self.milk >= 100:
                self.go_to_farm(grid, breeder_salary_evolution, algorithm_to_farm, mix_food_params)
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



    def move_towards(self, target, grid):
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

    def drink(self, grid, add_thirst):
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
                        
    def eating(self, grid, add_hunger):
        current_color = grid[self.x][self.y].color
        if current_color != "blue" and current_color != "gray":
            self.color_visit_count[current_color] += 1
            self.hunger += add_hunger
            self.hunger = min(self.hunger, 100)
        return
 

class Farm:
    def __init__(self, canvas, pre, nb_square, nb_cow, radius, color, dim_box, init_thirst, init_hunger, init_milk, init_salary, spacing):
        self.canvas = canvas
        self.pre = pre
        self.nb_square = nb_square
        self.breeder_salary = init_salary
        self.spacing = spacing
        self.cows = self.create_cows(nb_cow, radius, color, dim_box, init_thirst, init_hunger, init_milk, self.spacing)


    def create_cows(self, nb_cow, radius, color, dim_box, init_thirst, init_hunger, init_milk, spacing):
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
