from ast import List
import random
import tkinter as tk
from typing import Dict, List, Tuple

class Box:
    """
    This class is used to represent a box in the graphical interface.
    """


    def __init__(self, canvas: tk.Canvas, x: int, y: int, color: str, food_lifetime: float, time_to_recovery: int, square_length: int) -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.food_lifetime = food_lifetime
        self.has_cow = False
        self.rectangle_id = 0
        self.text_id = 0
        self.time_to_recovery = time_to_recovery
        self.square_length = square_length
        

    def update_color(self) -> None:
        """
        This method is used to update the color of the box.
        """

        self.canvas.itemconfig(self.text_id, text=str(self.food_lifetime))
        if self.time_to_recovery > 0 and self.color == "black":
            # print(self.x, self.y, "->", self.time_to_recovery)
            self.time_to_recovery -= 1


    def recolor(self, color: str, food_lifetime: float) -> None:
        """
        This method is used to recolor the box and update the food lifetime text.
        """
        self.color = color
        self.food_lifetime = food_lifetime
        self.time_to_recovery = 6
        
        # Mettre à jour la couleur du rectangle
        self.canvas.itemconfig(self.rectangle_id, fill=self.color)
        
        # Supprimer l'ancien texte s'il existe
        if hasattr(self, 'text_id') and self.text_id is not None:
            self.canvas.delete(self.text_id)

        
        # Obtenez les coordonnées du rectangle
        coords = self.canvas.coords(self.rectangle_id)
        
        # Vérifiez que les coordonnées sont suffisantes
        if len(coords) >= 4:
            x0, y0, x1, y1 = coords[:4]  # Utilisez les deux premiers points du rectangle
            text_x = x0 + self.square_length - ((0.9 * self.square_length) - 3)
            text_y = y0
            font_size = int((0.1 * self.square_length) + 4)  # Convertir font_size en int
        
            # Créer un nouveau texte avec le food_lifetime mis à jour
            self.text_id = self.canvas.create_text(
                text_x, text_y, text=str(self.food_lifetime), anchor=tk.NE, font=("Helvetica", font_size)
            )
        else:
            print("Erreur: Les coordonnées du rectangle ne sont pas suffisantes. <@box.recolor>")


    def set_color(self, new_color: str) -> None:
        """
        This method is used to set the color of the box.
        """

        self.color = new_color
        self.canvas.itemconfig(self.rectangle_id, fill=self.color)



def colorized_box(mix_food_params: Dict[str, Dict[str, str | int | float]], nb_square_per_line: int) -> List[Tuple[str, float, int]]:
    """
    This function is used to colorize the boxes.
    """
    total_squares = nb_square_per_line * nb_square_per_line - 1  # We subtract 1 for the special gray box
    
    colors = []

    cumulative_total = 0
    cumulative_ratio = 0.0

    for _, params in mix_food_params.items():
        mix_ratio = params["mix"]
        
        # Calculate the cumulative ratio
        cumulative_ratio += float(mix_ratio)
        cumulative_count = round(cumulative_ratio * total_squares)
        
        # Calculate the count for this color
        count = cumulative_count - cumulative_total
        cumulative_total += count
        
        
        color = params["color"]
        food_lifetime = params["food_lifetime"]
        time_to_recovery = params["time_to_recovery"]
        
        colors.extend([(color, food_lifetime, time_to_recovery)] * count)

    


    if (cumulative_total < total_squares) or (len(colors) != total_squares):
        print(f"Cumulative total is less than total squares: {cumulative_total} < {total_squares}")
        raise ValueError("Cumulative total is less than total squares.")
    
    random.shuffle(colors)
    return colors




def box_creation(canvas: tk.Canvas, pre: List, square_length: int, spacing: int, mix_food_params: Dict[str, Dict[str, str | int | float]], nb_square: int) -> None:
    """
    This function is used to create the boxes.
    """
    nb_square = len(pre[0])
    colored_boxes = colorized_box(mix_food_params, nb_square)

    if len(colored_boxes) != nb_square * nb_square - 1:
        print("Erreur: Les cases colorées ne correspondent pas au nombre de cases.")
        print(f"Nombre de cases colorées: {len(colored_boxes)} pour {nb_square * nb_square - 1} cases.")
        raise ValueError("Erreur: Les cases colorées ne correspondent pas au nombre de cases.")

    for i in range(nb_square):
        for j in range(nb_square):
            x0, y0 = i * (square_length + spacing) + spacing, j * (square_length + spacing) + spacing  # Position de départ de la case avec un espacement
            x1, y1 = x0 + square_length, y0 + square_length  # Taille de la case
            if i == 0 and j == nb_square // 2:
                box = Box(canvas, i, j, color="gray", food_lifetime=float('inf'), time_to_recovery=-1, square_length=square_length)
            else:
                color, food_lifetime, time_to_recovery = colored_boxes.pop(0)
                box = Box(canvas, i, j, color, food_lifetime, time_to_recovery + 1, square_length)
            box.rectangle_id = canvas.create_rectangle(x0, y0, x1, y1, fill=box.color)  # Stocke l'identifiant du rectangle
            
            if box.color not in ["blue", "gray"]:
                text_x = x0 + square_length - ((0.9 * square_length) - 3)
                text_y = y0
                font_size = int((0.1 * square_length) + 4)  # Convertir font_size en int

                box.text_id = canvas.create_text(
                    text_x, text_y, text=str(food_lifetime), anchor=tk.NE, font=("Helvetica", font_size)
                )  # Création du texte

            pre[i][j] = box  # Stockage de la case dans la grille