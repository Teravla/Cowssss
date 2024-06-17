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

        init_params = config_data.get("init_parameter", {}) 
        cow_params = config_data.get("cow_evolution", {})
        victory_params = config_data.get("victory_condition", {})
        algorithm_params = config_data.get("algorithm", {})
        analysis_params = config_data.get("analysis", {})
        food_value_params = config_data.get("food_value", [])

        self.square_length = init_params["square_lenght"]
        self.nb_square = init_params["number_of_squares"]
        self.spacing = init_params["spacing"]
        self.number_cows = init_params["number_of_cows"]
        
        self.hunger_cow = init_params["hunger_cow"]
        self.thirst_cow = init_params["thirst_cow"]
        self.milk_cow = init_params["milk_cow"]
        self.breeder_salary = init_params["breeder_salary"]

        self.hunger_evolution = cow_params["hunger_evolution"]
        self.thirst_evolution = cow_params["thirst_evolution"]
        self.milk_evolution = cow_params["milk_evolution"]
        self.add_hunger = cow_params["add_hunger"]
        self.add_thirst = cow_params["add_thirst"]
        self.breeder_salary_evolution = cow_params["breeder_salary_evolution"]
        self.number_ticks = init_params["number_ticks"]

        self.hunger_to_milk = victory_params["hunger_to_milk"]
        self.thirst_to_milk = victory_params["thirst_to_milk"]

        self.algorithm_to_farm = algorithm_params["to_farm"]

        self.show_analysis = analysis_params["show_analysis"]

        # Calculer les pourcentages de mixage des aliments
        self.mix_food_params = self.parse_food_values(food_value_params)

        if self.show_analysis:
            self.csv_filepath = create_csv()

        super().__init__()
        self.initialize()
        self.start_simulation()



    def parse_food_values(self, food_value_params):
        food_dict = {}

        for item in food_value_params:
            name = item["Type of Food"]
            food_value = item["Food Value"]
            milk_value = item["Milk Value"]
            cow_lifetime = item["Cow Lifetime"]
            time_to_recovery = item["Time to Recovery"]
            color = item["Color"]
            mix = item["Mix"]
            quality = item["Quality"]

            food_dict[name] = {"color": color, "mix": mix, "food_value": food_value, "milk_value": milk_value, "cow_lifetime": cow_lifetime, "time_to_recovery": time_to_recovery, "quality": quality}

        return food_dict

        


    def initialize(self):
        

        self.title("Simulation de vaches")

        # Détermination de la taille de l'écran et du canevas
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # paramètres des carrés
        if self.nb_square % 2 == 0:
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

        box_creation(self.canvas, self.pre, self.square_length, self.spacing, self.mix_food_params)

        self.farm = Farm(self.canvas, self.pre, self.nb_square, self.number_cows, self.square_length // 2, "black", self.square_length, self.hunger_cow, self.thirst_cow, self.milk_cow, self.breeder_salary, self.spacing)
        self.cows = self.farm.cows


    def start_simulation(self):
        response = messagebox.askyesno("Démarrer la simulation", "Voulez-vous démarrer la simulation ?")
        if response:
            self.simulation_running = True  # Ajout de l'attribut pour indiquer que la simulation est en cours
            self.tick()
        else:
            self.destroy()
            exit()

        



    def tick(self):
        if self.simulation_running:
            self.nb_tour += 1
            csv_filepath = self.csv_filepath if self.show_analysis else None
            
            simulate_tick(
                self.cows, self.pre, self.nb_tour,
                self.hunger_evolution, self.thirst_evolution, self.milk_evolution,
                self.add_hunger, self.add_thirst, self.breeder_salary_evolution,
                self.hunger_to_milk, self.thirst_to_milk, self.algorithm_to_farm,
                csv_filepath, self.show_analysis, self.mix_food_params
            )

            # Vérifiez si la simulation est terminée (par exemple, si toutes les vaches sont mortes)
            if not self.cows:
                self.simulation_running = False
                
                # Affiche l'analyse du fichier CSV si show_analysis est True
                if self.show_analysis:
                    print("Analyse du fichier :", self.csv_filepath)
                    analysis_result(self.csv_filepath)
                else:
                    
                    exit()
            else:
                self.after(self.number_ticks, self.tick)




if __name__ == "__main__":
    app = InterfaceGraphique()
    app.mainloop()
