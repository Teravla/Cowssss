import csv
import matplotlib.pyplot as plt

def analysis_result(filepath):
    data = {}  # Dictionnaire pour stocker toutes les données par ID
    ids = []   # Liste pour stocker les IDs dans l'ordre de lecture
    attributes = ['x', 'y', 'HUNGER', 'THIRST', 'MILK']  # Attributs à analyser

    # Lecture du fichier CSV
    with open(filepath, 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')

        for row in csvreader:
            tour_cow_id = row['ID']

            # Si l'ID n'est pas déjà dans le dictionnaire, l'ajouter avec un dictionnaire vide
            if tour_cow_id not in data:
                data[tour_cow_id] = {}

            # Ajouter toutes les données pour cet ID
            for key, value in row.items():
                if key != 'ID':  # Ne pas inclure l'ID dans les données individuelles
                    if key not in data[tour_cow_id]:
                        data[tour_cow_id][key] = []
                    data[tour_cow_id][key].append(int(value))

            # Si l'ID n'est pas déjà dans la liste des IDs, l'ajouter
            if tour_cow_id not in ids:
                ids.append(tour_cow_id)

    # Ordonner les IDs par numéro de tour
    ids = sorted(ids, key=lambda x: int(x.split('-')[0]))

    # Création du graphique combiné
    plt.figure(figsize=(12, 8))

    for attribute in attributes:
        values = [data[id][attribute][0] for id in ids]  # Extraire les valeurs pour chaque attribut
        plt.plot(ids, values, label=attribute)

    plt.xlabel('ID')
    plt.ylabel('Valeur')
    plt.title('Évolution des attributs des vaches au fil du temps')
    plt.xticks(rotation=45)  # Rotation des étiquettes des IDs
    plt.legend()
    plt.tight_layout()
    plt.show()