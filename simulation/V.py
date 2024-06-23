import random
import shutil
import sys
import os
import json
from typing import Any, Dict, List
from multiprocessing import Manager, Process
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import InterfaceGraphique

max_salary_tt = 0

class ModifierJson: 
    def __init__(self, nom_fichier: str):
        self.nom_fichier = nom_fichier

    def charger_json(self) -> Dict[str, Any]:
        with open(self.nom_fichier, 'r') as f:
            data = json.load(f)
        return data

    def modifier_nombre_vaches(self, nouveau_nombre_vaches: int) -> None:
        data = self.charger_json()
        data['init_parameter']['number_of_cows'] = nouveau_nombre_vaches
        with open(self.nom_fichier, 'w') as f:
            json.dump(data, f, indent=4)

    def change_config(self, config_filename: str, id: int) -> str:
        # Lire le fichier JSON
        with open(config_filename, 'r') as f:
            config_data = json.load(f)
        
        # Extraire les valeurs de "Mix" et identifier celles à modifier
        mix_values = [food['Mix'] for food in config_data['food_value'] if food['Type of Food'] != 'Water']
        water_mix = [food['Mix'] for food in config_data['food_value'] if food['Type of Food'] == 'Water'][0]

        # Modifier aléatoirement les valeurs de "Mix" pour les aliments autres que "Water"
        new_mix_values = [max(0, min(1, mix + random.uniform(-0.2, 0.2))) for mix in mix_values]

        # Ajuster les valeurs de "Mix" pour s'assurer que la somme est égale à 1
        total_mix = sum(new_mix_values) + water_mix
        adjustment_factor = (1 - water_mix) / sum(new_mix_values)
        adjusted_mix_values = [mix * adjustment_factor for mix in new_mix_values]

        # Arrondir les valeurs à trois chiffres après la virgule
        rounded_mix_values = [round(mix, 3) for mix in adjusted_mix_values]

        # Correction finale pour que la somme fasse exactement 1 après l'arrondi
        total_rounded_mix = sum(rounded_mix_values) + round(water_mix, 3)
        discrepancy = 1 - total_rounded_mix

        # Ajouter la différence à l'un des éléments pour corriger la somme
        if discrepancy != 0:
            for i in range(len(rounded_mix_values)):
                if rounded_mix_values[i] + discrepancy >= 0 and rounded_mix_values[i] + discrepancy <= 1:
                    rounded_mix_values[i] += discrepancy
                    break

        # Mettre à jour les valeurs de "Mix" dans les données de configuration
        mix_index = 0
        for food in config_data['food_value']:
            if food['Type of Food'] != 'Water':
                food['Mix'] = rounded_mix_values[mix_index]
                mix_index += 1

        # Créer le répertoire config_out s'il n'existe pas
        output_dir = os.path.join(os.path.dirname(__file__), 'config_out')
        os.makedirs(output_dir, exist_ok=True)

        # Définir le nom du fichier de sortie
        file_out = os.path.join(output_dir, f'file_out_{id}.json')

        # Écrire les modifications dans le fichier JSON file_out
        with open(file_out, 'w') as f:
            json.dump(config_data, f, indent=4)

        return file_out


class NeuralNetwork:


    def __init__(self, config_filename: str, modifier: ModifierJson, instance_id: int) -> None:
        self.instance_id = instance_id
        self.config_filename = modifier.change_config(config_filename, self.instance_id)


    def start_simulation(self) -> 'InterfaceGraphique':
        interface = InterfaceGraphique(self.config_filename, False, False)
        return interface

    def get_breeder_salary(self, interface: 'InterfaceGraphique') -> float:
        return interface.get_breeder_salary()
    
    def get_cow_id_death(self, interface: 'InterfaceGraphique') -> List[int] | None:
        return interface.get_cow_id_death()
    
    def get_cow_reason_death(self, interface: 'InterfaceGraphique') -> List[str] | None:
        return interface.get_cow_reason_death()
    
    def get_instance_id(self) -> int:
        return self.instance_id
    
    def write_salary_to_json(self, salary: float, id_startNN: int) -> None:
        results_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results.json'))

        # Vérifiez si le fichier JSON existe et n'est pas vide
        if os.path.exists(results_filename) and os.path.getsize(results_filename) > 0:
            with open(results_filename, 'r') as f:
                try:
                    results_data = json.load(f)
                except json.JSONDecodeError:
                    results_data = {}
        else:
            results_data = {}

        # Créez la structure si elle n'existe pas
        if f"Id_StartNN_{id_startNN}" not in results_data:
            results_data[f"Id_StartNN_{id_startNN}"] = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "instance": {}
            }

        # Ajoutez le salaire pour cette instance sous "Id_StartNN_{id_startNN}"
        instance_key = f"Instance_{self.instance_id}"
        salary = round(salary, 2)
        results_data[f"Id_StartNN_{id_startNN}"]["instance"][instance_key] = {
            "salary": salary
        }

        with open(results_filename, 'w') as f:
            json.dump(results_data, f, indent=4)


class StartNN:
    instance_counter = 1

    def __init__(self, config_file: str, iterations: int, nb_cow_init: int, results_filename: str):
        self.init_counter(results_filename)
        self.config_filename = config_file
        self.iterations = iterations
        self.nb_cow_init = nb_cow_init
        self.id = StartNN.instance_counter
        StartNN.instance_counter += 1
        self.results_filename = results_filename
        self.max_salary = 0

    @staticmethod
    def init_counter(results_filename: str) -> None:
        if os.path.exists(results_filename):
            with open(results_filename, 'r') as f:
                results_data = json.load(f)
                max_id = 0
                for key in results_data.keys():
                    if key.startswith("Id_StartNN_"):
                        try:
                            id_num = int(key.split("_")[-1])
                            if id_num > max_id:
                                max_id = id_num
                        except ValueError:
                            continue
                StartNN.instance_counter = max_id + 1 if max_id > 0 else 1
        else:
            StartNN.instance_counter = 1

    def start(self) -> None:
        modifier = ModifierJson(self.config_filename)
        modifier.modifier_nombre_vaches(self.nb_cow_init)

        with Manager() as manager:
            result_dict = manager.dict()  # Créer un dictionnaire partagé

            processes = []
            for i in range(self.iterations):
                process = Process(target=self.simulate_in_process, args=(i + 1, modifier, result_dict))
                process.start()
                processes.append(process)

            for process in processes:
                process.join()

            # Convertir le dictionnaire partagé en dictionnaire régulier
            result_dict = dict(result_dict)
        
        # Appeler reniew_json pour mettre à jour config.json
        self.reniew_json(self.results_filename, self.config_filename)

    def simulate_in_process(self, instance_id: int, modifier: ModifierJson, result_dict: Dict[int, float]) -> None:
        nn = NeuralNetwork(self.config_filename, modifier, instance_id)
        interface = nn.start_simulation()

        def simulate():
            salary = nn.get_breeder_salary(interface)
            if interface.simulation_running:
                interface.after(100, simulate)
            else:
                cow_id = nn.get_cow_id_death(interface)
                reason_death = nn.get_cow_reason_death(interface)
                # if cow_id is not None and reason_death is not None:
                #     for cow_id, reason_death in zip(cow_id, reason_death):
                #         if reason_death == "hunger":
                #             print(f"I{instance_id} - C{cow_id} - {reason_death}")
                nn.write_salary_to_json(salary, self.id)
                result_dict[instance_id] = salary
                interface.quit()

        interface.after(0, simulate)
        interface.mainloop()


    def reniew_json(self, results_filename: str, config_filename: str) -> None:
        global max_salary_tt  # Utiliser la variable globale max_salary_tt

        # Charger le dictionnaire des résultats
        with open(results_filename, 'r') as f:
            results_data = json.load(f)

        # Filtrer les résultats pour l'instance actuelle
        instance_key = f"Id_StartNN_{self.id}"
        if instance_key not in results_data:
            print(f"Aucun résultat trouvé pour l'instance {self.id}")
            return

        instance_data = results_data[instance_key]

        # Trouver l'instance avec le salaire le plus élevé
        max_salary = 0
        max_salary_sub_instance = None

        for sub_instance_key, sub_instance_data in instance_data["instance"].items():
            salary = sub_instance_data["salary"]
            if salary > max_salary:
                max_salary = salary
                max_salary_sub_instance = sub_instance_key

        if max_salary_sub_instance is None:
            print(f"Aucune sous-instance trouvée avec un salaire pour l'instance {self.id}.")
            return

        self.max_salary = max_salary

        if max_salary > max_salary_tt:
            max_salary_tt = max_salary
            # Construire le chemin du fichier de configuration de la sous-instance
            config_out_dir = os.path.join(os.path.dirname(__file__), 'config_out')
            sub_instance_number = max_salary_sub_instance.split('_')[-1]
            max_salary_config_file = os.path.join(config_out_dir, f'file_out_{sub_instance_number}.json')

            # Copier le fichier de configuration pour remplacer config.json
            shutil.copy(max_salary_config_file, config_filename)
    
    def get_max_salary(self) -> float:
        return self.max_salary


def write_max_salary_to_json(max_salary: float):
    # Définir le format de la date et obtenir la date actuelle
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Créer le dictionnaire à écrire dans le fichier JSON
    data = {
        "datetime": current_datetime,
        "max_salary": max_salary
    }

    # Déterminer le chemin du fichier où écrire les données
    output_filename = 'max_salary_record.json'  # Nom du fichier de sortie
    output_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), output_filename))

    # Écrire les données dans le fichier JSON
    with open(output_filepath, 'w') as f:
        json.dump(data, f, indent=4)

def create_missing_directories():
    # Liste des répertoires à vérifier et créer si nécessaire
    directories = [
        'data',
        'simulation',
        'simulation/algorithm',
        'simulation/config_out',
    ]

    # Parcourir chaque répertoire et créer s'il n'existe pas
    for directory in directories:
        directory_path = os.path.join(os.path.dirname(__file__), directory)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Répertoire créé : {directory_path}")

if __name__ == "__main__":
    create_missing_directories()
    config_filename = 'config.json'
    results_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results.json'))
    iterations = 3  # Nombre d'instances à créer
    nb_cow_init = 20  # Nombre initial de vaches
    max_salary = 0
    new_max_salary = 0

    for i in range(20):
        startNN = StartNN(config_filename, iterations, nb_cow_init, results_filename)
        startNN.start()
        new_max_salary = startNN.get_max_salary()
        if new_max_salary > max_salary:
            max_salary = new_max_salary
        print(f"{i} - {new_max_salary}")
        new_max_salary = 0

    print(f"Le salaire le plus élevé est de : {max_salary}")

    # Appeler la fonction pour écrire le maximum de salaire dans le fichier JSON
    write_max_salary_to_json(max_salary)

        
