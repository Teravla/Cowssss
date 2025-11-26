#!/bin/bash

# ---------------------------
# Chemins des projets
# ---------------------------
FILE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$FILE_DIR/Backend"
echo "Backend directory: $BACKEND_DIR (content : $(ls $BACKEND_DIR))"
FRONTEND_DIR="$FILE_DIR/Frontend"
echo "Frontend directory: $FRONTEND_DIR (content : $(ls $FRONTEND_DIR))"
BACKEND_PKG="$BACKEND_DIR/pkg"
FRONTEND_PKG="$FRONTEND_DIR/pkg"

# ---------------------------
# Fonction pour build le backend et copier pkg
# ---------------------------
build_backend() {
    echo "[Rust] Compilation du backend..."
    cd "$BACKEND_DIR" || exit
    wasm-pack build --target web --out-dir pkg
    echo "[Rust] Copie du pkg vers le frontend..."
    rm -rf "$FRONTEND_PKG"
    cp -r "$BACKEND_PKG" "$FRONTEND_PKG"
    cd - >/dev/null || exit
}

# ---------------------------
# Lancer le frontend npm avec hot reload
# ---------------------------
run_frontend() {
    echo "[Frontend] Lancement du serveur npm..."
    cd "$FRONTEND_DIR" || exit
    ls
    npm run dev
}

# ---------------------------
# Surveiller le backend avec cargo-watch
# ---------------------------
watch_backend() {
    echo "[Rust] Surveillance des fichiers Rust..."
    cargo watch -q -w "$BACKEND_DIR/src" -s "bash -c 'build_backend'"
}

# ---------------------------
# Exécution principale
# ---------------------------

# 1️⃣ Build initial
build_backend

# 2️⃣ Lancer npm frontend en arrière-plan
run_frontend & FRONTEND_PID=$!

# 3️⃣ Surveiller le backend Rust
watch_backend

# 4️⃣ Cleanup
trap "echo 'Arrêt du frontend...'; kill $FRONTEND_PID; exit 0" SIGINT
wait
