#!/bin/bash

# Setup script for OVH VPS deployment
# This script sets up the VPS environment for running the Freqtrade bot

set -e

echo "Setting up Freqtrade Bot on OVH VPS..."

# Update system
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker and Docker Compose
echo "Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker Compose v2
sudo apt-get install -y docker-compose

# Create freqtrade user
echo "Creating freqtrade user..."
sudo useradd -m -s /bin/bash freqtrade
sudo usermod -aG docker freqtrade

# Create application directory
echo "Setting up application directory..."
sudo mkdir -p /home/freqtrade/AI-Trading
sudo chown -R freqtrade:freqtrade /home/freqtrade/AI-Trading

# Create environment file template
echo "Creating environment file template..."
sudo tee /home/freqtrade/.env.template > /dev/null <<EOF
# Binance API credentials
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Telegram bot credentials
TELEGRAM_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
EOF

sudo chown freqtrade:freqtrade /home/freqtrade/.env.template

# Install systemd service
echo "Installing systemd service..."
sudo cp deployment/freqtrade.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable freqtrade

# Create log directory
sudo mkdir -p /var/log/freqtrade
sudo chown freqtrade:freqtrade /var/log/freqtrade

# Setup firewall (optional)
echo "Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 8080/tcp  # For FreqUI if needed
sudo ufw --force enable

echo "VPS setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy your .env file to /home/freqtrade/.env with your actual API keys"
echo "2. Deploy your application code to /home/freqtrade/AI-Trading"
echo "3. Create config.live.json from config.live.template.json"
echo "4. Start the service: sudo systemctl start freqtrade"
echo "5. Check status: sudo systemctl status freqtrade"
echo "6. View logs: journalctl -u freqtrade -f"