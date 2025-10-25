# core/apps.py
"""
App launcher utilities for Nova voice assistant.
Currently supports VS Code on Windows, macOS, and Linux.
"""

import os
import subprocess
import platform
import logging

def openVSCode():
    """Open Visual Studio Code safely on any OS."""
    try:
        system = platform.system().lower()

        if system == "windows":
            # Default install path
            path = r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv("USERNAME"))
            if os.path.exists(path):
                os.startfile(path)
            else:
                # If not found, try command-line fallback
                subprocess.Popen("code", shell=True)
        elif system == "darwin":  # macOS
            subprocess.Popen(["open", "-a", "Visual Studio Code"])
        else:  # Linux and others
            subprocess.Popen(["code"])
        return True

    except Exception:
        logging.exception("Failed to open VS Code.")
        return False
