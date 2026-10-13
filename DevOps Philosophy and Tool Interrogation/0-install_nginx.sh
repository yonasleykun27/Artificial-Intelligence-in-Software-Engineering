#!/usr/bin/env bash
# Imperative configuration script: Installs and configures Nginx web server
# Demonstrates "HOW" to achieve the state through sequential command execution

set -e

echo "[+] Updating apt repositories..."
apt-get update -y

echo "[+] Installing Nginx package..."
apt-get install -y nginx

echo "[+] Ensuring web root directory exists..."
if [ ! -d "/var/www/html" ]; then
    mkdir -p /var/www/html
fi

echo "[+] Writing default index.html content..."
echo "Holberton School" > /var/www/html/index.html

echo "[+] Checking if custom 404 redirection header is configured..."
CONFIG_FILE="/etc/nginx/sites-available/default"
if ! grep -q "rewrite ^/redirect_me https://www.youtube.com permanent;" "$CONFIG_FILE"; then
    echo "[+] Injecting redirect rule into Nginx configuration..."
    sed -i '/server_name _;/a \\n\trewrite ^/redirect_me https://www.youtube.com permanent;' "$CONFIG_FILE"
fi

echo "[+] Testing Nginx configuration syntax..."
nginx -t

echo "[+] Restarting Nginx daemon..."
service nginx restart

echo "[✓] Imperative execution completed successfully."
