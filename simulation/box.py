import random
import tkinter as tk

class Box:
    def __init__(self, canvas, x, y, color, food_lifetime, buffer):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.food_lifetime = food_lifetime
        self.has_cow = False
        self.rectangle_id = None  # Identifiant du rectangle dans l'interface graphique
        self.text_id = None  # Identifiant du texte affichant food_lifetime
        self.buffer_after_eating = buffer

    def update_color(self):
        # Mettre uniquement à jour le texte sur les cases
        self.canvas.itemconfig(self.text_id, text=str(self.food_lifetime))
        if self.buffer_after_eating > 0 and self.color == "black":
            self.buffer_after_eating -= 1
    
    def recolor(self, color):
        self.color = color
        self.canvas.itemconfig(self.rectangle_id, fill=self.color)  # Met à jour la couleur de la case dans l'interface graphique

            


        
    def set_color(self, new_color):
        self.color = new_color
        self.canvas.itemconfig(self.rectangle_id, fill=self.color)  # Met à jour la couleur de la case dans l'interface graphique

def colorized_box(mix_food_params, nb_square_per_line):
    total_squares = nb_square_per_line * nb_square_per_line
    colors = []

    # Calculer le nombre de cases pour chaque type de nourriture en fonction des proportions
    for food_type, params in mix_food_params.items():
        mix_ratio = params["mix"]
        count = int(total_squares * mix_ratio)
        color = params["color"]
        food_lifetime = params["food_lifetime"]
        colors.extend([(color, food_lifetime)] * count)
    
    random.shuffle(colors)
    return colors

def box_creation(canvas, pre, square_length, spacing, mix_food_params):
    nb_square = len(pre[0])
    colored_boxes = colorized_box(mix_food_params, nb_square)
    
    for i in range(nb_square):
        for j in range(nb_square):
            x0, y0 = i * (square_length + spacing) + spacing, j * (square_length + spacing) + spacing  # Position de départ de la case avec un espacement
            x1, y1 = x0 + square_length, y0 + square_length  # Taille de la case
            if i == 0 and j == nb_square // 2:
                box = Box(canvas, i, j, color="gray", food_lifetime=float('inf'), buffer=-1)
            else:
                color, food_lifetime = colored_boxes.pop(0)
                box = Box(canvas, i, j, color, food_lifetime, buffer=-1)
            
            box.rectangle_id = canvas.create_rectangle(x0, y0, x1, y1, fill=box.color)  # Stocke l'identifiant du rectangle
            
            if box.color != "gray":
                text_x = x0 + square_length - 15 
                text_y = y0 

                box.text_id = canvas.create_text(text_x, text_y, text=str(food_lifetime), anchor=tk.NE, font=("Helvetica", 6))  # Création du texte
            pre[i][j] = box  # Stockage de la case dans la grille
