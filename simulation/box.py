from ast import List
import random
import tkinter as tk
from typing import List

class Box:
    """
    This class is used to represent a box in the graphical interface.
    """


    def __init__(self, canvas: tk.Canvas, x: int, y: int, color: str, food_lifetime: float, time_to_recovery: int) -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.food_lifetime = food_lifetime
        self.has_cow = False
        self.rectangle_id = 0
        self.text_id = 0
        self.time_to_recovery = time_to_recovery


    def update_color(self) -> None:
        """
        This method is used to update the color of the box.
        """

        self.canvas.itemconfig(self.text_id, text=str(self.food_lifetime))
        if self.time_to_recovery > 0 and self.color == "black":
            self.time_to_recovery -= 1


    def recolor(self, color: str, food_lifetime: float) -> None:
        """
        This method is used to recolor the box and update the food lifetime text.
        """
        self.color = color
        self.food_lifetime = food_lifetime
        self.time_to_recovery = -1
        
        # Mettre à jour la couleur du rectangle
        self.canvas.itemconfig(self.rectangle_id, fill=self.color)
        
        # Supprimer l'ancien texte s'il existe
        if hasattr(self, 'text_id') and self.text_id is not None:
            print(f"Suppression de l'ancien texte {self.text_id} contenant {self.food_lifetime}")
            self.canvas.delete(self.text_id)

        
        # Obtenez les coordonnées du rectangle
        coords = self.canvas.coords(self.rectangle_id)
        
        # Vérifiez que les coordonnées sont suffisantes
        if len(coords) >= 4:
            x0, y0, x1, y1 = coords[:4]  # Utilisez les deux premiers points du rectangle
            text_x = x1 - 15  # Déterminez x pour le texte
            text_y = y0       # Déterminez y pour le texte
        
            # Créer un nouveau texte avec le food_lifetime mis à jour
            self.text_id = self.canvas.create_text(
                text_x, text_y, text=str(self.food_lifetime), anchor=tk.NE, font=("Helvetica", 6)
            )
        else:
            print("Erreur: Les coordonnées du rectangle ne sont pas suffisantes.")


    def set_color(self, new_color: str) -> None:
        """
        This method is used to set the color of the box.
        """
        print(f"Changing color of box at {self.x}, {self.y} to {new_color}.")
        self.color = new_color
        self.canvas.itemconfig(self.rectangle_id, fill=self.color)


def colorized_box(mix_food_params: dict[str, dict[str, str | int | float]], nb_square_per_line: int) -> list[tuple[str, float, int]]:
    """
    This function is used to colorize the boxes.
    """

    total_squares = nb_square_per_line * nb_square_per_line
    colors = []

    for _, params in mix_food_params.items():
        mix_ratio = params["mix"]
        count = int(total_squares * mix_ratio)
        color = params["color"]
        food_lifetime = params["food_lifetime"]
        time_to_recovery = params["time_to_recovery"]
        colors.extend([(color, food_lifetime, time_to_recovery)] * count)
    
    random.shuffle(colors)
    return colors


def box_creation(canvas: tk.Canvas, pre: List, square_length: int, spacing: int, mix_food_params: dict[str, dict[str, str | int | float]]) -> None:
    """
    This function is used to create the boxes.
    """
    
    nb_square = len(pre[0])
    colored_boxes = colorized_box(mix_food_params, nb_square)
    
    for i in range(nb_square):
        for j in range(nb_square):
            x0, y0 = i * (square_length + spacing) + spacing, j * (square_length + spacing) + spacing  # Position de départ de la case avec un espacement
            x1, y1 = x0 + square_length, y0 + square_length  # Taille de la case
            if i == 0 and j == nb_square // 2:
                box = Box(canvas, i, j, color="gray", food_lifetime=float('inf'), time_to_recovery=-1)
            else:
                color, food_lifetime, time_to_recovery = colored_boxes.pop(0)
                box = Box(canvas, i, j, color, food_lifetime, time_to_recovery)
            box.rectangle_id = canvas.create_rectangle(x0, y0, x1, y1, fill=box.color)  # Stocke l'identifiant du rectangle
            
            if box.color != "gray":
                text_x = x0 + square_length - ((0.9 * square_length) - 3)
                text_y = y0
                font_size = int((0.1 * square_length) + 4)  # Convertir font_size en int

                box.text_id = canvas.create_text(
                    text_x, text_y, text=str(food_lifetime), anchor=tk.NE, font=("Helvetica", font_size)
                )  # Création du texte

            pre[i][j] = box  # Stockage de la case dans la grille