#!/usr/bin/env python3
"""
AVRCP Play/Pause to Mute Menu Bar App
Uses MediaPlayer framework - this was working at 21:18:21!
"""

import logging
import subprocess
import sys
import os
import objc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/.cmon-sony.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

from Foundation import NSObject
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSVariableStatusItemLength
from PyObjCTools import AppHelper
import MediaPlayer

_controller = None
is_muted = False
status_item = None
status_menu_item = None


def toggle_mute():
    """Toggle mute state."""
    global is_muted, status_item, status_menu_item
    is_muted = not is_muted

    if is_muted:
        logger.info("=== MUTING ===")
        subprocess.run(["osascript", "-e", "set volume output muted true"], capture_output=True)
        logger.info("Headphones muted")
        if status_item:
            status_item.setTitle_("🔇")
        if status_menu_item:
            status_menu_item.setTitle_("Status: MUTED")
        mute_zoom()
    else:
        logger.info("=== UNMUTING ===")
        subprocess.run(["osascript", "-e", "set volume output muted false"], capture_output=True)
        logger.info("Headphones unmuted")
        if status_item:
            status_item.setTitle_("🎙")
        if status_menu_item:
            status_menu_item.setTitle_("Status: Unmuted")
        unmute_zoom()


def mute_zoom():
    try:
        script = '''
        tell application "System Events"
            if exists (process "zoom.us") then
                tell process "zoom.us"
                    set wins to (windows whose name contains "Zoom Meeting" or name contains "zoom share")
                    if (count of wins) > 0 then
                        keystroke "a" using {command down, shift down}
                    end if
                end tell
            end if
        end tell
        '''
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=2)
    except:
        pass


def unmute_zoom():
    try:
        script = '''
        tell application "System Events"
            if exists (process "zoom.us") then
                tell process "zoom.us"
                    set wins to (windows whose name contains "Zoom Meeting" or name contains "zoom share")
                    if (count of wins) > 0 then
                        keystroke "a" using {command down, shift down}
                    end if
                end tell
            end if
        end tell
        '''
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=2)
    except:
        pass


def handle_play(event):
    logger.info(">>> Play command received! <<<")
    toggle_mute()
    return MediaPlayer.MPRemoteCommandHandlerStatusSuccess


def handle_pause(event):
    logger.info(">>> Pause command received! <<<")
    toggle_mute()
    return MediaPlayer.MPRemoteCommandHandlerStatusSuccess


def handle_toggle(event):
    logger.info(">>> Toggle Play/Pause command received! <<<")
    toggle_mute()
    return MediaPlayer.MPRemoteCommandHandlerStatusSuccess


def setup_menu_bar():
    """Set up menu bar icon."""
    global status_item, status_menu_item

    status_bar = NSStatusBar.systemStatusBar()
    status_item = status_bar.statusItemWithLength_(NSVariableStatusItemLength)
    status_item.setTitle_("🎙")

    menu = NSMenu.alloc().init()

    status_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Status: Unmuted", None, ""
    )
    status_menu_item.setEnabled_(False)
    menu.addItem_(status_menu_item)

    menu.addItem_(NSMenuItem.separatorItem())

    quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit", "terminate:", "q"
    )
    menu.addItem_(quit_item)

    status_item.setMenu_(menu)
    logger.info("Menu bar setup complete")


def setup_media_commands():
    """Set up MediaPlayer remote command handlers."""
    command_center = MediaPlayer.MPRemoteCommandCenter.sharedCommandCenter()

    # Play
    play_cmd = command_center.playCommand()
    play_cmd.setEnabled_(True)
    play_cmd.addTargetWithHandler_(handle_play)

    # Pause
    pause_cmd = command_center.pauseCommand()
    pause_cmd.setEnabled_(True)
    pause_cmd.addTargetWithHandler_(handle_pause)

    # Toggle
    toggle_cmd = command_center.togglePlayPauseCommand()
    toggle_cmd.setEnabled_(True)
    toggle_cmd.addTargetWithHandler_(handle_toggle)

    # Set Now Playing info
    now_playing = {
        MediaPlayer.MPMediaItemPropertyTitle: "Sony Mute Control",
        MediaPlayer.MPMediaItemPropertyArtist: "cmon-sony",
        MediaPlayer.MPNowPlayingInfoPropertyPlaybackRate: 1.0,
    }
    MediaPlayer.MPNowPlayingInfoCenter.defaultCenter().setNowPlayingInfo_(now_playing)

    logger.info("Media command handlers registered")


def main():
    logger.info("=" * 50)
    logger.info("Starting AVRCP Menu Bar App (MediaPlayer version)")
    logger.info("=" * 50)

    app = NSApplication.sharedApplication()

    setup_menu_bar()
    setup_media_commands()

    logger.info("App running. Press play/pause on headphones to toggle mute.")

    AppHelper.runEventLoop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
