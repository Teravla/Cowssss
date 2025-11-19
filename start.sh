#!/bin/bash

# Chemins relatifs
BACKEND_PKG="./Backend/pkg"
FRONTEND_PKG="./Frontend/pkg"

cd ./Backend 
wasm-pack build --target web
cd ..

# Copier le contenu du pkg dans le frontend
echo "Copie des fichiers wasm vers le frontend..."
rm -rf "$FRONTEND_PKG"
cp -r "$BACKEND_PKG" "$FRONTEND_PKG"

# Lancer un serveur local dans le frontend
echo "Lancement du serveur local..."
cd ./Frontend || exit
npx serve .
