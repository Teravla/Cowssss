import torch

print(torch.cuda.is_available())

# Vérifie si CUDA (et donc ROCm) est disponible
if torch.cuda.is_available():
    # Obtenez la propriété du premier périphérique CUDA disponible
    device = torch.device("cuda:0")  # Sélectionne le premier périphérique CUDA
    properties = torch.cuda.get_device_properties(device)
    print(f"Nom du périphérique: {properties}")

    # Vérifie si le fabricant est AMD
    if properties.name.startswith("AMD"):
        print("Une carte graphique AMD ROCm est disponible.")
    else:
        print("Une carte graphique CUDA est disponible mais n'est pas AMD ROCm.")
else:
    print("Aucune carte graphique compatible CUDA (ou ROCm) n'est disponible.")

# Sélectionnez le périphérique CUDA si disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Utilisation du périphérique: {device}")

