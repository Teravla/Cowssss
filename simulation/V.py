import sys
import os
import json
import random
from typing import Any, Dict
import tkinter as tk
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import InterfaceGraphique

class ModifierJson: 
    def __init__(self, nom_fichier: str):
        self.nom_fichier = nom_fichier

    def charger_json(self) -> Dict[str, Any]:
        with open(self.nom_fichier, 'r') as f:
            data = json.load(f)
        return data

    def modifier_nombre_vaches(self, nouveau_nombre_vaches: int) -> None:
        # Charger les données JSON
        data = self.charger_json()
        
        # Modifier le nombre de vaches
        data['init_parameter']['number_of_cows'] = nouveau_nombre_vaches
        
        # Écrire les modifications dans le fichier JSON
        with open(self.nom_fichier, 'w') as f:
            json.dump(data, f, indent=4)

class NeuralNetwork:
    instance_counter = 1  # Variable statique pour le compteur d'instances

    def __init__(self, config_filename: str):
        self.config_filename = config_filename
        self.instance_id = NeuralNetwork.instance_counter
        NeuralNetwork.instance_counter += 1

    def start_simulation(self) -> tk.Tk:
        print(f"Démarrage de la simulation pour l'instance {self.instance_id}")
        interface = InterfaceGraphique(self.config_filename, False)
        return interface

    def get_breeder_salary(self, interface) -> float:
        return interface.get_breeder_salary()

def simulate_in_thread(nn: NeuralNetwork):
    interface = nn.start_simulation()

    def simulate():
        print(f"Simulation pour l'instance {nn.instance_id}")
        salary = nn.get_breeder_salary(interface)
        print(f"\nSalaire pour l'instance {nn.instance_id}: {salary}\n")
        interface.quit()  # Assurer que mainloop se termine après l'obtention du salaire

    # Utiliser after pour démarrer la simulation après un délai
    simulate()
    print(f"Simulation démarrée pour l'instance {nn.instance_id}")
    interface.mainloop()

def StartNN(config_filename: str, iterations: int, nb_cow_init) -> None:
    threads = []

    # Modifier le JSON avant de démarrer les threads
    modifier = ModifierJson(config_filename)
    modifier.modifier_nombre_vaches(nb_cow_init)

    # Démarrer les threads de simulation
    for _ in range(iterations):
        nn = NeuralNetwork(config_filename)
        thread = threading.Thread(target=simulate_in_thread, args=(nn,))
        thread.start()
        threads.append(thread)

    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    config_filename = 'config.json'
    StartNN(config_filename, 1, 1)
