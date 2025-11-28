# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

cmon-sony is a macOS menu bar daemon that intercepts Sony WH-1000XM5 headphone play/pause button presses and converts them into mute toggles for both system audio and Zoom.

## Commands

```bash
# Install and start daemon
./setup.sh

# View logs
tail -f /tmp/cmon-sony.log

# Stop/start/restart daemon
launchctl unload ~/Library/LaunchAgents/com.cmon.sony.plist
launchctl load ~/Library/LaunchAgents/com.cmon.sony.plist

# Check if running
launchctl list | grep cmon
```

## Architecture

Single-file Python daemon (`avrcp_daemon.py`) using PyObjC:

- **Media command interception**: Registers with `MPRemoteCommandCenter` to capture AVRCP play/pause/toggle commands from Bluetooth headphones
- **Menu bar UI**: `NSStatusBar` status item showing mute state (🔊/🔇)
- **Mute actions**: Toggles system audio via AppleScript, sends Cmd+Shift+A to Zoom via AppleScript accessibility

The daemon runs as a launchd service (`com.cmon.sony.plist`) configured via `setup.sh`, which generates the plist with correct Python and script paths.

## Key Dependencies

- `pyobjc-framework-MediaPlayer` for AVRCP command handling
- PyObjC's AppKit bindings for menu bar and event loop
