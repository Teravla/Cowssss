import tkinter as tk
from tkinter import messagebox
from simulation.box import box_creation
from simulation.cow import Cow, create_cows
from simulation.simulate_cow import simulate_tick


class InterfaceGraphique(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulation de vaches")

        # Détermination de la taille de l'écran et du canevas
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # paramètres des carrés
        square_length = 20
        if square_length % 2 != 0:
            square_length += 1

        nb_square = 10
        if nb_square % 2 != 0:
            nb_square += 1

        spacing = 10

        self.nb_tour = 0

        # Calcul de la taille du canevas
        canvas_width = nb_square * (square_length + spacing) + spacing
        canvas_height = nb_square * (square_length + spacing) + spacing

        # Calcul du positionnement pour centrer la fenêtre
        window_width = canvas_width + 20  # Largeur de la fenêtre
        window_height = canvas_height + 20 # Hauteur de la fenêtre
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Positionnement de la fenêtre au centre de l'écran
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Création du canevas
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Placement du canevas au centre de la fenêtre

        self.pre = [[None for _ in range(nb_square)] for _ in range(nb_square)]  # Grille de nb_square x nb_square pour stocker les cases

        box_creation(self.canvas, self.pre, 0.98, square_length, spacing)

        self.cows = create_cows(self.canvas, self.pre, nb_square, 9, 8, "black", square_length, spacing)  # Création des vaches avec un rayon de 8

        # Demande à l'utilisateur de démarrer la simulation
        self.start_simulation()

    def start_simulation(self):
        response = messagebox.askyesno("Démarrer la simulation", "Voulez-vous démarrer la simulation ?")
        if response:
            print(f"Nombre de vaches : {len(self.cows)}")
            print(f"vaches : {self.cows}")
            self.tick()



    def tick(self):
        
        print(f"Tour {self.nb_tour}")
        self.nb_tour += 1
        simulate_tick(self.cows, self.pre)  # Passer la liste des vaches et la grille à la fonction simulate_tick
        self.after(1000, self.tick)

if __name__ == "__main__":
    app = InterfaceGraphique()
    app.mainloop()
