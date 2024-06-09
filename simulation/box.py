import random
import tkinter as tk

class Box:
    def __init__(self, canvas, x, y, color="white", has_cow=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.has_cow = False

def colorized_box(percentage, nb_square_per_line):
    # Répartition des couleurs
    total_squares = nb_square_per_line * nb_square_per_line
    green_count = int(total_squares * percentage)  # Nombre de cases vertes
    blue_count = total_squares - green_count  # Nombre de cases bleues
    colors = ["green"] * green_count + ["blue"] * blue_count
    random.shuffle(colors)
    return colors


def box_creation(canvas, pre, percentage, square_length, spacing):
    nb_square = len(pre[0])
    colors = colorized_box(percentage, nb_square) 
    
    for i in range(nb_square):
        for j in range(nb_square):
            x0, y0 = i * (square_length + spacing) + spacing, j * (square_length + spacing) + spacing  # Position de départ de la case avec un espacement
            x1, y1 = x0 + square_length, y0 + square_length  # Taille de la case
            box = Box(canvas, i, j, colors[i * nb_square + j])  # Création d'une nouvelle case avec ses coordonnées et sa couleur
            canvas.create_rectangle(x0, y0, x1, y1, fill=box.color)  # Colorisation de la case avec sa couleur
            pre[i][j] = box  # Stockage de la case dans la grille
