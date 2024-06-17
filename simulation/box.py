import random
import tkinter as tk

class Box:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.has_cow = False
        self.turns_since_yellow = 0  # Compteur pour suivre les tours depuis que la case est jaune
        self.rectangle_id = None  # Identifiant du rectangle dans l'interface graphique

    def update_color(self):
        # if self.color == "yellow":
        #     if self.turns_since_yellow == 10:
        #         self.color = "green"
        #         self.canvas.itemconfig(self.rectangle_id, fill="green")  # Met à jour la couleur de la case dans l'interface graphique
        #         self.turns_since_yellow = 0  # Réinitialise le compteur après avoir changé la couleur à vert
        #     self.turns_since_yellow += 1
        pass

def colorized_box(mix_food_params, nb_square_per_line):
    total_squares = nb_square_per_line * nb_square_per_line
    colors = []

    # Calculer le nombre de cases pour chaque type de nourriture en fonction des proportions
    for food_type, params in mix_food_params.items():
        mix_ratio = params["mix"]
        count = int(total_squares * mix_ratio)
        color = params["color"]
        colors.extend([color] * count)
    
    random.shuffle(colors)
    return colors



def box_creation(canvas, pre, square_length, spacing, mix_food_params):
    nb_square = len(pre[0])
    colors = colorized_box(mix_food_params, nb_square)
    
    for i in range(nb_square):
        for j in range(nb_square):
            x0, y0 = i * (square_length + spacing) + spacing, j * (square_length + spacing) + spacing  # Position de départ de la case avec un espacement
            x1, y1 = x0 + square_length, y0 + square_length  # Taille de la case
            if i == 0 and j == nb_square // 2:
                box = Box(canvas, i, j, color="gray")  # Crée une case grise aux coordonnées spécifiées
            else:
                box = Box(canvas, i, j, colors.pop(0))
            box.rectangle_id = canvas.create_rectangle(x0, y0, x1, y1, fill=box.color)  # Stocke l'identifiant du rectangle
            pre[i][j] = box  # Stockage de la case dans la grille


