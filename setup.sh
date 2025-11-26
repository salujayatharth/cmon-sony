#!/bin/bash
# Setup script for AVRCP daemon

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLIST_FILE="$PROJECT_DIR/com.cmon.sony.plist"
DAEMON_SCRIPT="$PROJECT_DIR/avrcp_daemon.py"
LAUNCHD_PATH="$HOME/Library/LaunchAgents/com.cmon.sony.plist"

echo "Installing AVRCP daemon..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --break-system-packages -r "$PROJECT_DIR/requirements.txt"

# Make daemon script executable
chmod +x "$DAEMON_SCRIPT"

# Install launchd plist
echo "Installing launchd service..."
cp "$PLIST_FILE" "$LAUNCHD_PATH"
chmod 644 "$LAUNCHD_PATH"

# Load the service
echo "Loading service..."
launchctl load "$LAUNCHD_PATH"

echo "Setup complete! The daemon will start automatically."
echo "To check status: launchctl list | grep com.cmon.sony"
echo "To view logs: tail -f ~/.cmon-sony.log"
echo "To stop: launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist"
