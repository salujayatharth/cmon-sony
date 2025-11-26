#!/usr/bin/env python3
"""
Sony WH1000XM5 AVRCP Mute Control Daemon
Listens for play/pause and toggles system audio mute + Zoom mute.
Background only - no UI.
"""

import logging
import subprocess
import sys
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('/tmp/cmon-sony.log')]
)
logger = logging.getLogger(__name__)

from AppKit import NSApplication
from PyObjCTools import AppHelper
import MediaPlayer

is_muted = False


def toggle_mute():
    global is_muted
    is_muted = not is_muted

    if is_muted:
        logger.info("MUTING")
        subprocess.run(["osascript", "-e", "set volume output muted true"], capture_output=True)
        mute_zoom()
    else:
        logger.info("UNMUTING")
        subprocess.run(["osascript", "-e", "set volume output muted false"], capture_output=True)
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
    logger.info("Play command received")
    toggle_mute()
    return MediaPlayer.MPRemoteCommandHandlerStatusSuccess


def handle_pause(event):
    logger.info("Pause command received")
    toggle_mute()
    return MediaPlayer.MPRemoteCommandHandlerStatusSuccess


def handle_toggle(event):
    logger.info("Toggle command received")
    toggle_mute()
    return MediaPlayer.MPRemoteCommandHandlerStatusSuccess


def setup_media_commands():
    cc = MediaPlayer.MPRemoteCommandCenter.sharedCommandCenter()

    cc.playCommand().setEnabled_(True)
    cc.playCommand().addTargetWithHandler_(handle_play)

    cc.pauseCommand().setEnabled_(True)
    cc.pauseCommand().addTargetWithHandler_(handle_pause)

    cc.togglePlayPauseCommand().setEnabled_(True)
    cc.togglePlayPauseCommand().addTargetWithHandler_(handle_toggle)

    MediaPlayer.MPNowPlayingInfoCenter.defaultCenter().setNowPlayingInfo_({
        MediaPlayer.MPMediaItemPropertyTitle: "Mute Control",
        MediaPlayer.MPNowPlayingInfoPropertyPlaybackRate: 1.0,
    })

    logger.info("Media handlers registered")


def main():
    logger.info("Starting cmon-sony daemon")

    NSApplication.sharedApplication()
    setup_media_commands()

    logger.info("Listening for play/pause...")
    AppHelper.runEventLoop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
