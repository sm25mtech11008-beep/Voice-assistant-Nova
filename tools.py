# core/tools.py
import pywhatkit
import wikipedia
import random
import logging
from core.speech import speak

def playOnYouTube(query):
    """Play a YouTube video for the given query or random choice from list."""
    try:
        if isinstance(query, list):
            query = random.choice(query)
        speak(f"Playing {query} on YouTube.")
        pywhatkit.playonyt(query)
    except Exception:
        logging.exception("Failed to play video on YouTube.")
        speak("Sorry, I couldn't play that on YouTube right now.")

def searchWikipedia(query):
    """Search Wikipedia and return a short summary."""
    try:
        speak("Searching Wikipedia...")
        topic = query.replace("wikipedia", "").strip()
        results = wikipedia.summary(topic, sentences=2)
        speak("According to Wikipedia.")
        speak(results)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        option = e.options[0]
        speak(f"There are multiple results. Showing the first: {option}.")
        return option
    except Exception:
        logging.exception("Wikipedia search failed.")
        speak("Sorry, I couldn't find anything on Wikipedia.")
        return None
