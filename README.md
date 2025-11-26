# cmon-sony

A macOS background daemon that turns your Sony WH-1000XM5 headphones' play/pause button into a universal mute toggle.

## What it does

Press play/pause on your Sony headphones to:
- Toggle system audio mute
- Toggle Zoom microphone mute (if in a meeting)

Works via AVRCP (Bluetooth media controls) using macOS MediaPlayer framework.

## Requirements

- macOS 12+
- Python 3.9+ (via Homebrew)
- Sony WH-1000XM5 headphones (other AVRCP-compatible headphones may work)

## Installation

```bash
git clone https://github.com/salujayatharth/cmon-sony.git
cd cmon-sony
./setup.sh
```

The setup script will:
1. Install Python dependencies
2. Copy the launchd plist to `~/Library/LaunchAgents/`
3. Start the daemon

## Permissions

You'll need to grant:
- **Accessibility**: For sending keystrokes to Zoom (`System Settings > Privacy & Security > Accessibility`)

## Usage

Just press play/pause on your Sony headphones. The daemon toggles mute state on each press.

## Commands

```bash
# View logs
tail -f /tmp/cmon-sony.log

# Stop daemon
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist

# Start daemon
launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist

# Restart daemon
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist && \
launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist

# Check status
launchctl list | grep cmon
```

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist
rm ~/Library/LaunchAgents/com.cmon.sony.plist
```

## How it works

The daemon registers as a media command handler using macOS's `MPRemoteCommandCenter`. When you press play/pause on your headphones, macOS routes the AVRCP command to this daemon, which then:

1. Toggles system audio mute via AppleScript
2. Sends `Cmd+Shift+A` to Zoom if a meeting window is open

## License

MIT
