#!/bin/bash
# Setup script for cmon-sony daemon

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DAEMON_SCRIPT="$PROJECT_DIR/avrcp_daemon.py"
LAUNCHD_PATH="$HOME/Library/LaunchAgents/com.cmon.sony.plist"
PYTHON_PATH=$(which python3)

echo "Installing cmon-sony daemon..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --break-system-packages -r "$PROJECT_DIR/requirements.txt" 2>/dev/null || \
pip3 install -r "$PROJECT_DIR/requirements.txt"

# Make daemon script executable
chmod +x "$DAEMON_SCRIPT"

# Generate launchd plist with correct paths
echo "Creating launchd service..."
cat > "$LAUNCHD_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cmon.sony</string>

    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_PATH}</string>
        <string>${DAEMON_SCRIPT}</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/tmp/cmon-sony.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/cmon-sony.log</string>
</dict>
</plist>
EOF

chmod 644 "$LAUNCHD_PATH"

# Unload if already running
launchctl unload "$LAUNCHD_PATH" 2>/dev/null || true

# Load the service
echo "Starting daemon..."
launchctl load "$LAUNCHD_PATH"

echo ""
echo "Setup complete!"
echo "View logs:  tail -f /tmp/cmon-sony.log"
echo "Stop:       launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist"
echo "Restart:    launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist && launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist"
