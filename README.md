# Cowssss

## Un programme de simulation des besoins d'une vache dans un environnement contrôlé. Saurez-vous optimiser les revenus de l'éleveur ?

________

### Le champs

Le champs contient les cases suivantes:

    - Des cases vertes --> les cases d'herbes tant raffolé par nos amis les vaches
    - Des cases bleues --> des cases d'eau (imprevisible n'est-ce pas?)
    - Une case grise --> la ferme

________

### Les vaches

Les vaches sont des êtres simples et globalement, dans ce modèle, non dotés de capacité de reflexion. Toutefois, elles ont des besoins qu'il faut absolument assouvir, sinon, notre pauvre eleveur ne récoltera pas de lait.

Les vaches possedent les attributs suivants:

    - Une jauge de faim
    - Une jauge de soif
    - Une jauge de capacité laitière

Chaque tick (1 tick = unité de temps du modèle), la vache peut faire l'une de ces actions par ordre de priorité:

    - Se déplacer d'une case vers la source si elle a soif (jauge < 50%)
    - Se déplacer d'une case vers le pré le plus proche si elle a faim (jauge < 50%)
    - Mourir si ses besoin ne sont pas remplis

De plus, chaque tick, les évènements suivants se passent:

    - Chaque vache perd 10% de faim
    - Chaque vache perd 10% de soif
    - Chaque vache gagne 5% de lait

Quoiqu'il se passe, les vaches produisent du lait si leur jauge de faim et de soif sont > 80%. Elle peuvent être traite à n'importe quel moment. Toutefois, la vache doit se rendre à la ferme pour être trait selon les conditions suivantes:

    - Une vache pleine à plus de 90% de lait se déplace de 1 case tout les 5 tick
    - Une vache pleine à 80% de lait se déplace d'une case tout les 4 tick
    - Une vache pleine à 60% de lait se déplace d'une case tout les 3 tick
    - Une vache pleine à 40% de lait se déplace d'une case tout les 2 tick
    - Une vache pleine à moins de 20% de lait se déplace d'une case tout les 1 tick

Après 3 traites, les vaches meurent d'épuisement.

________

### Objectif du modèle

En partant de x vaches, voir comment une IA gérera la traite des vaches pour optimiser les revenus de l'eleveur en un temps imparti (1 minutes)
