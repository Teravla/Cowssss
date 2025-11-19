# CHANGELOG

________

## Version 0.1 (2024-09-06)

    - Ajout de la classe Cow pour représenter une vache dans la simulation.
    - Implémentation de la méthode __init__ de la classe Cow pour initialiser les attributs de la vache.
    - Implémentation de la méthode draw pour dessiner la vache sur le canevas avec un identifiant unique.
    - Implémentation des méthodes update_needs et make_milk pour mettre à jour les besoins de la vache et produire du lait en fonction de ses besoins en nourriture et en eau.
    - Implémentation des méthodes move, find_nearest, go_to_farm, move_to_farm, act, move_towards, drink et eating pour gérer le déplacement de la vache, la recherche des cases d'eau et d'herbe les plus proches, le déplacement vers la ferme pour la traite, le comportement de la vache pendant la simulation, la gestion du déplacement vers une cible et la consommation d'eau et d'herbe.
    - Ajout de la fonction create_cows pour créer les instances de vaches dans la simulation.
    - Ajout de la classe InterfaceGraphique pour gérer l'interface utilisateur de la simulation.
    - Implémentation des méthodes __init__, start_simulation, tick dans la classe InterfaceGraphique pour initialiser l'interface graphique, démarrer la simulation et avancer d'un tour.
    - Ajout de la fonction simulate_tick pour simuler un tour de la vache.
    - Ajout de la classe Box pour représenter une case sur le canevas.
    - Implémentation de la méthode update_color dans la classe Box pour mettre à jour la couleur de la case en fonction du temps écoulé depuis le changement de couleur.
    - Ajout de la fonction colorized_box pour générer une liste de couleurs pour les cases en fonction du pourcentage donné.
    - Ajout de la fonction box_creation pour créer les cases sur le canevas avec des couleurs différentes et une case grise spécifique aux coordonnées (0, nb_square//2).
    - Création du repo git et des fichiers correspondants

________

auteur : @teravla *(<teravla.pro@gmail.com>)*
