import tkinter as tk

class Cow:
    # Variable statique pour attribuer un identifiant unique à chaque vache
    cow_id_counter = 0

    def __init__(self, canvas, x, y, radius, color, dim_box):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius // 1.25
        self.color = color
        self.dim_box = dim_box
        self.tick_count = 0

        # Attributs des besoins de la vache
        self.hunger = 50  # Jauge de faim (0-100)
        self.thirst = 50  # Jauge de soif (0-100)
        self.milk = 0  # Jauge de capacité laitière (0-100)
        self.alive = True  # État de vie de la vache
        self.number_milking = 0  # Nombre de fois que la vache a été traitée

        # Salaire de l'eleveur
        self.breeder_salary = 0 

        # Attributs de l'identifiant de la vache
        self.id = Cow.cow_id_counter
        Cow.cow_id_counter += 1

        self.draw(self.radius, self.color, self.dim_box)

    def draw(self, radius, color, dim_box):
        # Calcul des coordonnées du centre du cercle
        center_x = self.x * 30 + dim_box
        center_y = self.y * 30 + dim_box
        # Dessin du cercle noir avec l'identifiant de la vache comme étiquette
        self.circle_id = self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill=color)

    def update_needs(self):
        # Exemple de mise à jour des besoins de la vache
        if self.thirst > 0 and self.hunger > 0:
            self.thirst -= 5
            self.hunger -= 5

        self.make_milk()  # Appel de la méthode pour produire du lait

        # Vache meurt si ses jauges sont à 0
        if self.hunger <= 0 or self.thirst <= 0:
            self.alive = False

    def make_milk(self):
        if self.alive and self.hunger > 80 and self.thirst > 90:
            self.milk += 10

    def move(self, dx, dy, grid):
        if self.alive:
            new_x = self.x + dx
            new_y = self.y + dy
            # Vérifie si la nouvelle position n'est pas une case bleue
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y].color != "blue":
                self.x = new_x
                self.y = new_y
                self.canvas.move(self.circle_id, dx * 30, dy * 30)  # Déplacer le cercle correspondant à la vache

    def find_nearest(self, grid, target_color):
        for radius in range(1, len(grid)):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    new_x, new_y = self.x + dx, self.y + dy
                    if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                        if grid[new_x][new_y].color == target_color:
                            return new_x, new_y
        return None

    def go_to_farm(self, grid):
        if self.alive:
            if self.milk >= 90:
                if self.tick_count % 5 == 0:
                    self.move_to_farm(grid)
            elif self.milk >= 80:
                if self.tick_count % 4 == 0:
                    self.move_to_farm(grid)
            elif self.milk >= 60:
                if self.tick_count % 3 == 0:
                    self.move_to_farm(grid)
            elif self.milk >= 40:
                if self.tick_count % 2 == 0:
                    self.move_to_farm(grid)
            elif self.milk >= 20:
                if self.tick_count % 1 == 0:
                    self.move_to_farm(grid)

    def move_to_farm(self, grid):
        farm_location = (0, len(grid) // 2)  # Coordonnées de la ferme
        current_location = (self.x, self.y)
        dx = farm_location[0] - current_location[0]
        dy = farm_location[1] - current_location[1]
        # Déplacer la vache d'une case vers la ferme
        self.move(dx, dy, grid)
        if self.x == farm_location[0] and self.y == farm_location[1]:
            self.number_milking += 1  # Incrémente le compteur de traite
            self.breeder_salary += 10 # Augmente le salaire de l'éleveur
            self.milk = 0  # Réinitialise la jauge de lait

    def act(self, grid):

        print(f"Salaire de l'éleveur : {self.breeder_salary}")
        self.tick_count += 1

        if self.number_milking >= 3:
            self.alive = False
            return

        if self.alive:
            print(f"Cow {self.id} is acting : hunger={self.hunger}, thirst={self.thirst}, milk={self.milk}")

            if self.milk >= 100:
                print(f"Cow {self.id} is going to the farm.")
                self.go_to_farm(grid)
                return
            else:
                if self.thirst < 90:
                    print(f"Cow {self.id} drinking water.")
                    target = self.find_nearest(grid, "blue")
                    if target:
                        self.move_towards(target, grid)
                        self.drink(grid)
                        self.update_needs()  # Met à jour les besoins après avoir bu
                        return  # Quitte après avoir bu
                elif self.hunger < 90:
                    print(f"Cow {self.id} eating grass.")
                    target = self.find_nearest(grid, "green")
                    if target:
                        self.move_towards(target, grid)
                        self.eating(grid)
                        self.update_needs()  # Met à jour les besoins après avoir mangé
                        return
                else:
                    print(f"Cow {self.id} is wandering.")
                    self.update_needs()
        


            



    def move_towards(self, target, grid):
        if target:
            target_x, target_y = target
            dx = 1 if target_x > self.x else -1 if target_x < self.x else 0
            dy = 1 if target_y > self.y else -1 if target_y < self.y else 0

            # Vérifie les mouvements possibles sans se déplacer vers une case bleue
            if 0 <= self.x + dx < len(grid) and 0 <= self.y + dy < len(grid[0]) and grid[self.x + dx][self.y + dy].color != "blue":
                self.move(dx, dy, grid)
            elif dx != 0 and 0 <= self.x + dx < len(grid) and grid[self.x + dx][self.y].color != "blue":
                self.move(dx, 0, grid)
            elif dy != 0 and 0 <= self.y + dy < len(grid[0]) and grid[self.x][self.y + dy].color != "blue":
                self.move(0, dy, grid)

    def drink(self, grid):
        if self.alive:
            # Vérifie si la vache est à proximité immédiate d'une case bleue
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Ignore la case où la vache se trouve actuellement
                    new_x, new_y = self.x + dx, self.y + dy
                    if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                        if grid[new_x][new_y].color == "blue":
                            # La vache boit de l'eau sans se déplacer sur la case bleue
                            self.thirst = 100
                            return  # Sort de la fonction après avoir bu
                        
    def eating(self, grid):
        if self.alive:
            # Vérifie si la vache est sur une case verte
            if 0 <= self.x < len(grid) and 0 <= self.y < len(grid[0]):
                if grid[self.x][self.y].color == "green":
                    # La vache mange
                    self.hunger += 20
                    self.hunger = min(self.hunger, 100)  # Assure que la faim ne dépasse pas 100
                    grid[self.x][self.y].color = "yellow"
                    self.canvas.itemconfig(grid[self.x][self.y].rectangle_id, fill="yellow")  # Met à jour la couleur de la case dans l'interface graphique
                    return  # Sort de la fonction après avoir mangé
 


def create_cows(canvas, pre, nb_square, nb_cow, radius, color, dim_box, spacing):
    coo_central_x = nb_square // 2
    coo_central_y = nb_square // 2

    # Fonction pour vérifier si une position est valide pour placer une vache
    def is_valid_position(x, y):
        return (0 <= x < nb_square and 0 <= y < nb_square and
                pre[x][y].color != "blue" and not pre[x][y].has_cow)

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
                        cow = Cow(canvas, x, y, radius, color, dim_box)
                        pre[x][y].has_cow = True
                        created_cows.append(cow)  # Ajout de la vache créée à la liste
                        placed = True
                        break
                if placed:
                    break
            search_radius += 1
            if search_radius > nb_square:
                break

        if not placed:
            print("Aucune position valide n'a été trouvée pour la vache.")

    return created_cows  # Retourner la liste des vaches créées
