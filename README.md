# cmon-sony

Background daemon that listens for play/pause from Sony WH1000XM5 headphones and toggles mute.

## Features

- Toggles system audio mute on play/pause
- Sends Cmd+Shift+A to Zoom to toggle mic mute in meetings
- Runs as background daemon via launchd
- Auto-starts on login

## Install

```bash
./setup.sh
```

## Usage

Press play/pause on your Sony headphones to toggle mute.

## Commands

```bash
# View logs
tail -f ~/.cmon-sony.log

# Stop
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist

# Start
launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist

# Restart
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist && launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist
```
