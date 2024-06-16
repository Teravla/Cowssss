import csv
import os
from datetime import datetime

def create_csv(filename=None):
    # Générer un nom de fichier unique basé sur l'horodatage
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f'{timestamp}.csv'
    
    # Obtenir le chemin absolu du répertoire courant
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_directory, filename)

    with open(filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')

        # En-têtes des colonnes
        headers = ['ID', 'x', 'y', 'HUNGER', 'THIRST', 'MILK']
        csvwriter.writerow(headers)
    
    return filepath  # Retourner le chemin du fichier pour l'utiliser plus tard


def append_to_csv(filepath, cows_data, nb_tour):
    with open(filepath, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')

        # Données par ligne (attributs des vaches par tour)
        for tour in range(len(cows_data)):
            for cow_id in cows_data[tour]:
                cow = cows_data[tour][cow_id]
                row_data = [
                    f'{nb_tour}-{cow_id}',
                    cow['x'],
                    cow['y'],
                    cow['hunger'],
                    cow['thirst'],
                    cow['milk']
                ]
                csvwriter.writerow(row_data)


def collect_cow_data(cows, nb_tour, all_cows_data):
    tour_data = {}
    for cow in cows:
        tour_data[cow.id] = {
            'x': cow.x,
            'y': cow.y,
            'hunger': cow.hunger,
            'thirst': cow.thirst,
            'milk': cow.milk
        }
    all_cows_data[nb_tour] = tour_data
    return all_cows_data


