import json
from datetime import datetime
from prisma.models import Cow, Farm  # Importez vos modèles Prisma générés

import csv
import os

def generate_csv_in_current_directory(filename, cows_data):
    # Obtenir le chemin absolu du répertoire courant
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_directory, filename)

    with open(filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')

        # En-têtes des colonnes
        headers = ['ID', 'x', 'y', 'HUNGER', 'THIRST']
        csvwriter.writerow(headers)

        # Données par ligne (attributs des vaches par tour)
        for tour in range(len(cows_data)):
            for cow_id in cows_data[tour]:
                cow = cows_data[tour][cow_id]
                row_data = [
                    f'{tour + 1}-{cow_id}',
                    cow['x'],
                    cow['y'],
                    cow['hunger'],
                    cow['thirst']
                ]
                csvwriter.writerow(row_data)

# Exemple de données des vaches par tour
cows_data = [
    {
        1: {'x': 10, 'y': 5, 'hunger': 80, 'thirst': 70},
        2: {'x': 15, 'y': 8, 'hunger': 60, 'thirst': 50},
    },
    {
        1: {'x': 11, 'y': 6, 'hunger': 70, 'thirst': 60},
        2: {'x': 14, 'y': 9, 'hunger': 50, 'thirst': 40},
    },
]

# Nom du fichier CSV à générer
filename = 'cows_data.csv'

# Générer le fichier CSV dans le répertoire courant
generate_csv_in_current_directory(filename, cows_data)
