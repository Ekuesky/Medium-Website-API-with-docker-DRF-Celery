#!/bin/bash

# Arrêt du script si une erreur survient
set -e

# Vérification des variables d'environnement nécessaires
if [ -z "$DIGITAL_OCEAN_IP_ADDRESS" ]; then
    echo "Error: DIGITAL_OCEAN_IP_ADDRESS not defined"
    exit 1
fi

# Vérification de la présence de git, rsync et ssh
command -v git >/dev/null 2>&1 || { echo "Error: git is required but not installed"; exit 1; }
command -v rsync >/dev/null 2>&1 || { echo "Error: rsync is required but not installed"; exit 1; }
command -v ssh >/dev/null 2>&1 || { echo "Error: ssh is required but not installed"; exit 1; }

# Configuration des variables
REMOTE_USER="root"
REMOTE_APP_DIR="/app"
REMOTE_TMP_DIR="/tmp"
BRANCH="main"

echo "🚀 Starting deployment process..."

# Création de l'archive du projet
echo "📦 Creating project archive..."
if ! git archive --format tar --output ./project.tar $BRANCH; then
    echo "Error: Failed to create project archive"
    exit 1
fi

# Upload du projet
echo "📤 Uploading project to server..."
if ! rsync -avz --progress ./project.tar $REMOTE_USER@$DIGITAL_OCEAN_IP_ADDRESS:$REMOTE_TMP_DIR/project.tar; then
    echo "Error: Failed to upload project"
    exit 1
fi

# Exécution des commandes sur le serveur
echo "🛠️  Building and deploying on server..."
ssh -o StrictHostKeyChecking=no $REMOTE_USER@$DIGITAL_OCEAN_IP_ADDRESS << ENDSSH
    set -e
    echo "Creating application directory..."
    mkdir -p /app

    echo "Extracting project files..."
    rm -rf /app/* && tar -xf /tmp/project.tar -C /app

    echo "Starting Docker containers..."
    cd /app
    docker compose -f production.yml pull
    docker compose -f production.yml up --build -d --remove-orphans

    echo "Cleaning up..."
    rm -f /tmp/project.tar
    docker system prune -f
ENDSSH

echo "✅ Deployment completed successfully!"

# Nettoyage local
rm -f ./project.tar