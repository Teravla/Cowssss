import tkinter as tk
from simulation.algorithm.algorithms import Algorithm
class Cow:
    # Variable statique pour attribuer un identifiant unique à chaque vache
    cow_id_counter = 0

    def __init__(self, canvas, x, y, radius, color, dim_box, init_thirst, init_hunger, init_milk, farm):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius // 1.25
        self.color = color
        self.dim_box = dim_box
        self.tick_count = 0
        self.path_to_farm = []

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
        center_x = self.x * 30 + dim_box
        center_y = self.y * 30 + dim_box
        # Dessin du cercle noir avec l'identifiant de la vache comme étiquette
        self.circle_id = self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=color)

    def update_needs(self, hunger_evolution, thirst_evolution, milk_evolution, hunger_to_milk, thirst_to_milk):
        # Exemple de mise à jour des besoins de la vache
        if self.thirst > 0 and self.hunger > 0:
            self.thirst -= thirst_evolution
            self.hunger -= hunger_evolution

        self.make_milk(milk_evolution, hunger_to_milk, thirst_to_milk)

        # Vache meurt si ses jauges sont à 0
        if self.hunger <= 0 or self.thirst <= 0:
            self.alive = False
            self.reason_death = "hunger" if self.hunger <= 0 else "thirst"

    def make_milk(self, milk_evolution, hunger_to_milk, thirst_to_milk):
        if self.alive and self.hunger >= hunger_to_milk and self.thirst >= thirst_to_milk:
            print(f"Vache {self.id} produit du lait.")
            self.milk += milk_evolution


    def find_nearest(self, grid, target_color):
        for radius in range(1, len(grid)):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    new_x, new_y = self.x + dx, self.y + dy
                    if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                        if grid[new_x][new_y].color == target_color:
                            return new_x, new_y
        return None

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
                    print(f"Vache {self.id} ne peut pas se déplacer sur une case occupée par une autre vache.")
            else:
                print(f"Vache {self.id} ne peut pas se déplacer sur la case bleue.")
                print(f"La case bleue est à la position ({new_x}, {new_y}) et la vache est à la position ({self.x}, {self.y}).")
                exit()

    def go_to_farm(self, grid, breeder_salary_evolution, algorithm):
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
                    self.number_milking += 1
                    self.farm.breeder_salary += breeder_salary_evolution
                    self.milk = 0
                    self.hunger = 20
                    self.thirst = 20
                    self.path_to_farm = []  # Réinitialise le chemin après l'arrivée


    def act(self, grid, nb_tour, hunger_evolution, thirst_evolution, milk_evolution, add_hunger, add_thirst, breeder_salary_evolution, hunger_to_milk, thirst_to_milk, algorithm_to_farm):


        print(f"Salaire de l'éleveur : {self.farm.breeder_salary}")
        self.tick_count += 1

        if self.number_milking >= 3:
            self.alive = False
            self.reason_death = "milking"
            return

        needs_updated = False  # Variable pour suivre si les besoins ont été mis à jour

        if self.alive and (0 <= self.x < len(grid) and 0 <= self.y < len(grid[0])):
            print(f"Début du tour {nb_tour} Cow {self.id} is acting : hunger={self.hunger}, thirst={self.thirst}, milk={self.milk}")

            if self.milk >= 100:
                print(f"Cow {self.id} is going to the farm.")
                self.go_to_farm(grid, breeder_salary_evolution, algorithm_to_farm)
                
            else:
                if self.thirst < thirst_to_milk:
                    print(f"Cow {self.id} drinking water.")
                    target = self.find_nearest(grid, "blue")
                    if target:
                        self.move_towards(target, grid)
                        self.drink(grid, add_thirst)
                        needs_updated = True
                elif self.hunger < hunger_to_milk:
                    print(f"Cow {self.id} eating grass.")
                    target = self.find_nearest(grid, "green")
                    if target:
                        self.move_towards(target, grid)
                        self.eating(grid, add_hunger)
                        needs_updated = True
                else:
                    print(f"Cow {self.id} is wandering.")
                    needs_updated = True

            if needs_updated:
                self.update_needs(hunger_evolution, thirst_evolution, milk_evolution, hunger_to_milk, thirst_to_milk)
                print(f"Fin du tour {nb_tour} Cow {self.id} is acting : hunger={self.hunger}, thirst={self.thirst}, milk={self.milk}\n")
                return


            
        


            



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
        if grid[self.x][self.y].color == "green":
            self.hunger += add_hunger
            self.hunger = min(self.hunger, 100)  # Assure que la faim ne dépasse pas 100
            grid[self.x][self.y].color = "yellow"
            self.canvas.itemconfig(grid[self.x][self.y].rectangle_id, fill="yellow")  # Met à jour la couleur de la case dans l'interface graphique
        return 
 

class Farm:
    def __init__(self, canvas, pre, nb_square, nb_cow, radius, color, dim_box, init_thirst, init_hunger, init_milk, init_salary):
        self.canvas = canvas
        self.pre = pre
        self.nb_square = nb_square
        self.breeder_salary = init_salary
        self.cows = self.create_cows(nb_cow, radius, color, dim_box, init_thirst, init_hunger, init_milk)

    def create_cows(self, nb_cow, radius, color, dim_box, init_thirst, init_hunger, init_milk):
        coo_central_x = self.nb_square // 2
        coo_central_y = self.nb_square // 2

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

                            cow = Cow(self.canvas, x, y, radius, color, dim_box, init_thirst, init_hunger, init_milk, self)

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
