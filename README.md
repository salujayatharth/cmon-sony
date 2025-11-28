# cmon-sony

A macOS menu bar app that turns your Sony WH-1000XM5 headphones' play/pause button into a universal mic mute toggle.

## What it does

Press play/pause on your Sony headphones to:
- Toggle system microphone mute
- Toggle Zoom mute (if in a meeting)

Works via AVRCP (Bluetooth media controls) using macOS MediaPlayer framework.

## Requirements

- macOS 12+
- Python 3.9+ (via Homebrew)
- Sony WH-1000XM5 headphones (other AVRCP-compatible headphones may work)

## Installation

### Homebrew (recommended)

```bash
brew tap salujayatharth/tap
brew install cmon-sony
brew services start cmon-sony
```

### Manual

```bash
git clone https://github.com/salujayatharth/cmon-sony.git
cd cmon-sony
./setup.sh
```

The setup script will install Python dependencies and configure the launchd service.

## Permissions

You'll need to grant:
- **Accessibility**: For sending keystrokes to Zoom (`System Settings > Privacy & Security > Accessibility`)

## Usage

Just press play/pause on your Sony headphones. The daemon toggles mute state on each press.

## Commands

### Homebrew install

```bash
brew services start cmon-sony   # Start
brew services stop cmon-sony    # Stop
brew services restart cmon-sony # Restart
tail -f /opt/homebrew/var/log/cmon-sony.log  # View logs
```

### Manual install

```bash
tail -f /tmp/cmon-sony.log  # View logs
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist  # Stop
launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist    # Start
launchctl list | grep cmon  # Check status
```

## Uninstall

### Homebrew
```bash
brew services stop cmon-sony
brew uninstall cmon-sony
```

### Manual
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
