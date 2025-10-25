# core/speech.py
import platform
import pyttsx3
import logging

def _init_engine():
    try:
        system = platform.system().lower()
        if system == "windows":
            return pyttsx3.init('sapi5')
        elif system == "darwin":
            return pyttsx3.init('nsss')
        else:
            return pyttsx3.init('espeak')
    except Exception:
        logging.exception("Failed to initialize pyttsx3 engine.")
        return None

engine = _init_engine()
if engine:
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)

def speak(text: str):
    """Convert text to speech."""
    if not engine:
        print(f"[speak disabled] {text}")
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        logging.exception("Speech synthesis failed.")

