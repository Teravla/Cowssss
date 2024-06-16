import tkinter as tk
from tkinter import messagebox
from data.result import create_csv
from simulation.box import box_creation
from simulation.cow import Farm
from simulation.simulate_cow import simulate_tick
from data.analysis_results import analysis_result
import json

class InterfaceGraphique(tk.Tk):
    def __init__(self, file: str = "./config.json"):
        self.nb_tour = 0
        self.config_file = file

        # Chargement des paramètres depuis le fichier JSON
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)

        init_params = config_data.get("init_paramter", {}) 
        cow_params = config_data.get("cow_evolution", {})
        victory_params = config_data.get("victory_condition", {})
        algorithm_params = config_data.get("algorithm", {})

        self.square_length = init_params.get("square_lenght", 20)
        self.nb_square = init_params.get("number_of_squares", 10)
        self.spacing = init_params.get("spacing", 10)
        self.number_cows = init_params.get("number_of_cows", 1)
        self.percentage_water = init_params.get("percentage_water", 0.98)
        self.hunger_cow = init_params.get("hunger_cow", 50)
        self.thirst_cow = init_params.get("thirst_cow", 50)
        self.milk_cow = init_params.get("milk_cow", 0)
        self.breeder_salary = init_params.get("breeder_salary", 0)

        self.hunger_evolution = cow_params.get("hunger_evolution", 5)
        self.thirst_evolution = cow_params.get("thirst_evolution", 5)
        self.milk_evolution = cow_params.get("milk_evolution", 10)
        self.add_hunger = cow_params.get("add_hunger", 20)
        self.add_thirst = cow_params.get("add_thirst", 100)
        self.breeder_salary_evolution = cow_params.get("breeder_salary_evolution", 10)
        self.number_ticks = init_params.get("number_ticks", 100)

        self.hunger_to_milk = victory_params.get("hunger_to_milk", 0.5)
        self.thirst_to_milk = victory_params.get("thirst_to_milk", 0.5)

        self.algorithm_to_farm = algorithm_params.get("to_farm", "dijkstra")
        

        self.csv_filepath = create_csv()

        super().__init__()
        self.initialize()
        self.start_simulation()
        

    def initialize(self):
        

        self.title("Simulation de vaches")

        # Détermination de la taille de l'écran et du canevas
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # paramètres des carrés
        if self.square_length % 2 != 0:
            self.square_length += 1
        if self.nb_square % 2 != 0:
            self.nb_square += 1

        # Calcul de la taille du canevas
        canvas_width = self.nb_square * (self.square_length + self.spacing) + self.spacing
        canvas_height = self.nb_square * (self.square_length + self.spacing) + self.spacing

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

        self.pre = [[None for _ in range(self.nb_square)] for _ in range(self.nb_square)]  # Grille de nb_square x nb_square pour stocker les cases

        box_creation(self.canvas, self.pre, self.percentage_water, self.square_length, self.spacing)

        self.farm = Farm(self.canvas, self.pre, self.nb_square, self.number_cows, self.square_length // 2, "black", self.square_length, self.hunger_cow, self.thirst_cow, self.milk_cow, self.breeder_salary)
        self.cows = self.farm.cows


    def start_simulation(self):
        response = messagebox.askyesno("Démarrer la simulation", "Voulez-vous démarrer la simulation ?")
        if response:
            self.simulation_running = True  # Ajout de l'attribut pour indiquer que la simulation est en cours
            self.csv_filepath = create_csv()  # Créez le fichier CSV au début de la simulation
            print(f"Nombre de vaches : {len(self.cows)}")
            print(f"vaches : {self.cows}")
            self.tick()
        else:
            self.destroy()
            exit()

        



    def tick(self):
        if self.simulation_running:
            self.nb_tour += 1
            simulate_tick(self.cows, self.pre, self.nb_tour, self.hunger_evolution, self.thirst_evolution, self.milk_evolution, self.add_hunger, self.add_thirst, self.breeder_salary_evolution, self.hunger_to_milk, self.thirst_to_milk, self.algorithm_to_farm, self.csv_filepath)

            # Vérifiez si la simulation est terminée (par exemple, si toutes les vaches sont mortes)
            if not self.cows:  # ou une autre condition de fin
                self.simulation_running = False  # Marquez la simulation comme terminée
                print("analyse du fichier : ", self.csv_filepath)
                analysis_result(self.csv_filepath)  # Appelez l'analyse des résultats
            else:
                self.after(self.number_ticks, self.tick)



if __name__ == "__main__":
    app = InterfaceGraphique()
    app.mainloop()
