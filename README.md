# AVRCP Play/Pause to Mute Daemon

A macOS daemon that listens for play/pause button presses on your Sony WH1000XM5 headphones and automatically toggles system mute/unmute.

## How It Works

1. Connects to your Sony WH1000XM5 headphones via Bluetooth
2. Monitors HID input events for AVRCP play/pause commands
3. When play/pause is pressed, toggles the system audio mute state
4. Runs continuously in the background as a launchd daemon

## Requirements

- macOS (tested on Sonoma)
- Python 3.8+
- Sony WH1000XM5 headphones paired and turned on

## Installation

1. Clone or download this project
2. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```

3. Run the setup script:
   ```bash
   ./setup.sh
   ```

This will:
- Install Python dependencies (bleak, aiohttp)
- Make the daemon script executable
- Install the launchd service
- Start the daemon automatically

## Usage

### Start the daemon
After installation, the daemon starts automatically on login.

To start manually:
```bash
launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist
```

### Stop the daemon
```bash
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist
```

### View logs
```bash
tail -f ~/.cmon-sony.log
```

### Check status
```bash
launchctl list | grep com.cmon.sony
ps aux | grep avrcp_daemon
```

### Run in foreground (for debugging)
```bash
python3 /path/to/avrcp_daemon.py
```

## How to Pair Headphones

1. Make sure your Sony WH1000XM5 are turned on
2. Open System Settings → Bluetooth
3. Put headphones in pairing mode (hold the power button)
4. Select "WH-1000XM5" from available devices
5. Click "Connect"

## Troubleshooting

### Daemon not starting
- Check logs: `tail -f ~/.cmon-sony.log`
- Make sure Python 3 is installed: `which python3`
- Verify launchd service is loaded: `launchctl list | grep com.cmon.sony`

### Headphones not detected
- Ensure headphones are turned on and in range
- Check Bluetooth settings in System Preferences
- Logs should show "Found device:" if paired and in range

### Play/pause not being detected
- The daemon may still be discovering the correct HID characteristic
- Check logs for "Subscribed to notifications:"
- You may need to adjust the HID code detection (0xcd for play/pause)

## Files

- `avrcp_daemon.py` - Main daemon script
- `requirements.txt` - Python dependencies
- `com.cmon.sony.plist` - launchd configuration
- `setup.sh` - Installation script

## Notes

- The daemon logs to `~/.cmon-sony.log`
- When muted, volume is set to 0
- When unmuted, volume is set to 50%
- The daemon automatically reconnects if the connection is lost
