# improved_main.py
"""
Robust entrypoint for Nova voice assistant.

Improvements vs original:
- guards against None returned from takeCommand()
- uses containment checks for wake/sleep phrases
- exception handling around microphone/recognition errors
- clean KeyboardInterrupt exit and optional debug logging
"""

import sys
import time
import logging
from core.listener import takeCommand
from core.speech import speak
from core.commands import executeCommand
from core.gpt_response import get_offline_reply

# wake/sleep phrases (lowercase)
WAKE_WORDS = ["hey nova", "wake up nova"]
SLEEP_WORDS = ["go to sleep", "stop listening", "sleep nova", "go to sleep nova"]

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def safe_listen():
    """
    Wrapper around takeCommand() to ensure we always return a normalized string.
    Returns empty string on errors or None responses so caller can continue.
    """
    try:
        result = takeCommand()
        if result is None:
            return ""
        # Ensure string and normalize
        return str(result).strip().lower()
    except Exception as e:
        logging.exception("Error while listening:")
        # small backoff to avoid tight error loop
        time.sleep(0.5)
        return ""


def passive_listen():
    logging.info("Nova is sleeping. Waiting for wake word...")
    try:
        while True:
            query = safe_listen()
            if not query:
                # nothing heard, continue listening
                continue

            # wake when any wake phrase appears anywhere in the recognized string
            if any(wake in query for wake in WAKE_WORDS):
                logging.info("Wake word detected.")
                try:
                    speak("Yes, I'm here!")
                except Exception:
                    logging.exception("TTS failed while responding to wake word.")
                active_listen()
                logging.info("Returned to passive listening.")
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting.")
        sys.exit(0)


def active_listen():
    logging.info("Nova is active now.")
    try:
        while True:
            query = safe_listen()
            if not query:
                # user didn't say anything meaningful
                continue

            # check for any sleep phrase contained in the query
            if any(sleep in query for sleep in SLEEP_WORDS):
                try:
                    speak("Going to sleep. Say 'Hey Nova' to wake me again.")
                except Exception:
                    logging.exception("TTS failed while going to sleep.")
                break

            # Try executing known commands
            try:
                success = executeCommand(query)
            except Exception:
                logging.exception("Error while executing command:")
                success = False

            # Fallback to offline GPT if command not recognized
            if not success:
                try:
                    response = get_offline_reply(query)
                except Exception:
                    logging.exception("Offline GPT fallback failed. Using default message.")
                    response = "Sorry, I couldn't process that."
                try:
                    speak(response)
                except Exception:
                    logging.exception("TTS failed when speaking GPT response.")

    except KeyboardInterrupt:
        logging.info("Interrupted by user while active. Returning to passive mode.")
    except Exception:
        logging.exception("Unhandled exception in active_listen(). Returning to passive.")


if __name__ == "__main__":
    passive_listen()
