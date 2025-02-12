#!/bin/bash

# Navigate to the application directory
cd /home/ec2-user/myapp

# Pull the latest changes from the main branch
git pull origin main

# Stop running containers
sudo docker-compose down

# Remove all unused containers, networks, images, and optionally, volumes
sudo docker system prune -a -f --volumes

# Build and start the containers
sudo docker-compose up --build -d