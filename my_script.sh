#!/bin/bash

# Script to update Docker and Docker Compose

# Constants
DOCKER_COMPOSE_VERSION="2.20.3"

# Function to check command existence
command_exists() {
    command -v "$1" &> /dev/null
}

# Update Docker
echo "Updating Docker..."
if command_exists apt-get; then
    sudo apt-get update
    sudo apt-get install --only-upgrade docker-ce docker-ce-cli containerd.io
elif command_exists brew; then
    brew update
    brew upgrade docker
else
    echo "Package manager not found. Please update Docker manually."
fi

# Update Docker Compose
echo "Updating Docker Compose to version $DOCKER_COMPOSE_VERSION..."
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Adjust permissions for docker-compose.yml
echo "Adjusting permissions for docker-compose.yml..."
chmod u+w docker-compose.yml

echo "Setup completed successfully."
