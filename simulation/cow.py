import tkinter as tk

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

        # Attributs des besoins de la vache
        self.hunger = 100  # Jauge de faim (0-100)
        self.thirst = 100  # Jauge de soif (0-100)
        self.milk = 0  # Jauge de capacité laitière (0-100)
        self.alive = True  # État de vie de la vache

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
        if self.thirst > 0:
            self.thirst -= 5
        else:
            self.hunger -= 5
        self.milk += 5
        # Vache meurt si ses jauges sont à 0
        if self.hunger <= 0 or self.thirst <= 0:
            self.alive = False

    def move(self, dx, dy):
        if self.alive:
            self.x += dx
            self.y += dy
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

    def act(self, grid):
        if self.alive:
            print(f"Cow {self.id} is acting.")
            if self.thirst < 50:
                target = self.find_nearest(grid, "blue")
                if target:
                    self.move_towards(target)
                    self.drink(grid)
            elif self.hunger < 50:
                target = self.find_nearest(grid, "green")
                if target:
                    self.move_towards(target)
            self.update_needs()

    def move_towards(self, target):
        if target:
            target_x, target_y = target
            dx = 1 if target_x > self.x else -1 if target_x < self.x else 0
            dy = 1 if target_y > self.y else -1 if target_y < self.y else 0
            self.move(dx, dy)

    def drink(self, grid):
        self.thirst += 20
        self.thirst = min(self.thirst, 100)
        x, y = self.x, self.y
        grid[x][y].color = "white"  # Faire disparaître la case d'eau



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
