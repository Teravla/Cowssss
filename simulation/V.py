import sys
import os
import json
from typing import Any, Dict, List
from multiprocessing import Process
from datetime import datetime

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
        data = self.charger_json()
        data['init_parameter']['number_of_cows'] = nouveau_nombre_vaches
        with open(self.nom_fichier, 'w') as f:
            json.dump(data, f, indent=4)

class NeuralNetwork:
    instance_counter = 1

    def __init__(self, config_filename: str):
        self.config_filename = config_filename
        self.instance_id = NeuralNetwork.instance_counter
        NeuralNetwork.instance_counter += 1

    def start_simulation(self) -> 'InterfaceGraphique':
        print(f"Démarrage de la simulation pour l'instance {self.instance_id}")
        interface = InterfaceGraphique(self.config_filename, False)
        return interface

    def get_breeder_salary(self, interface: 'InterfaceGraphique') -> float:
        return interface.get_breeder_salary()
    
    def get_cow_id_death(self, interface: 'InterfaceGraphique') -> List[int] | None:
        return interface.get_cow_id_death()
    
    def get_cow_reason_death(self, interface: 'InterfaceGraphique') -> List[str] | None:
        return interface.get_cow_reason_death()
    
    def write_salary_to_json(self, salary: float, id_startNN: int) -> None:
        results_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results.json'))

        if os.path.exists(results_filename):
            with open(results_filename, 'r') as f:
                results_data = json.load(f)
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


def simulate_in_process(config_filename: str, instance_id: int, id_startNN: int) -> None:
    nn = NeuralNetwork(config_filename)
    nn.instance_id = instance_id
    interface = nn.start_simulation()

    def simulate():
        salary = nn.get_breeder_salary(interface)
        if interface.simulation_running:
            interface.after(100, simulate)
        else:
            cow_id = nn.get_cow_id_death(interface)
            reason_death = nn.get_cow_reason_death(interface)
            if cow_id is not None and reason_death is not None:
                for cow_id, reason_death in zip(cow_id, reason_death):
                    print(f"I{instance_id} - C{cow_id} - {reason_death}")
                    # print(f"Cow {cow_id} has died by {reason_death} for the instance {nn.instance_id}")
            nn.write_salary_to_json(salary, id_startNN)
            print("Salaire pour l'instance {} : {:.2f}".format(nn.instance_id, salary))
            interface.quit()

    interface.after(0, simulate)
    interface.mainloop()

class StartNN:
    instance_counter = 1

    def __init__(self, config_filename: str, iterations: int, nb_cow_init: int, results_filename: str):
        self.init_counter(results_filename)
        self.config_filename = config_filename
        self.iterations = iterations
        self.nb_cow_init = nb_cow_init
        self.id = StartNN.instance_counter
        StartNN.instance_counter += 1

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

        processes = []
        for i in range(self.iterations):
            process = Process(target=simulate_in_process, args=(self.config_filename, i + 1, self.id))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()


if __name__ == "__main__":
    config_filename = 'config.json'
    results_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results.json'))
    iterations = 3  # Nombre d'instances à créer
    nb_cow_init = 1  # Nombre initial de vaches

    startNN = StartNN(config_filename, iterations, nb_cow_init, results_filename)
    startNN.start()
