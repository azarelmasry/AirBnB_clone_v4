#!/usr/bin/env bash
# This script sets up the web server for the deployment of web_static

# Update package information
sudo apt-get -y update

# Upgrade installed packages (optional, you can omit this if not needed)
sudo apt-get -y upgrade

# Install Nginx
sudo apt-get -y install nginx

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a simple test HTML file
echo "This is a test" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the 'test' release directory to serve as 'current'
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of the /data directory to the 'ubuntu' user and group
sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve the static files
nginx_config="/etc/nginx/sites-available/default"
nginx_location="\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"

# Add the location block to the Nginx default site configuration
# Make sure to check the line number for insertion (it might not be 38)
sudo sed -i "/^server {/a $nginx_location" $nginx_config

# Start Nginx
sudo service nginx start
