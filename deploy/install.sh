#!/bin/bash
set -e

echo "=== Installing Kofi Citizen Agent as systemd service ==="

# Kill any running nanobot gateway
pkill -f "nanobot gateway" 2>/dev/null || true
sleep 1

# Copy service file
sudo cp deploy/kofi-citizen.service /etc/systemd/system/kofi-citizen.service

# Reload systemd
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable kofi-citizen
sudo systemctl start kofi-citizen

echo ""
echo "=== Kofi is deployed! ==="
echo ""
echo "Commands:"
echo "  sudo systemctl status kofi-citizen   # Check status"
echo "  sudo journalctl -u kofi-citizen -f   # Follow logs"
echo "  sudo systemctl restart kofi-citizen   # Restart"
echo "  sudo systemctl stop kofi-citizen      # Stop"
