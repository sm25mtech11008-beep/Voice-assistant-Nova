# core/commands.py
import webbrowser
from datetime import datetime
import logging
from core.speech import speak
from core.tools import searchWikipedia, playOnYouTube
from core.apps import openVSCode
from core.intent import detectIntent
from core.gpt_module import ask_gpt

def executeCommand(query: str) -> bool:
    """
    Executes a command based on recognized user query.
    Returns:
        bool: True if a command was successfully executed, False otherwise.
    """
    if not query:
        return False

    query = query.lower()
    try:
        # --- Open websites ---
        sites = {
            "wikipedia": "https://www.wikipedia.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "twitter": "https://www.twitter.com",
            "stackoverflow": "https://stackoverflow.com",
            "linkedin": "https://www.linkedin.com",
            "whatsapp": "https://www.whatsapp.com",
            "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.com",
            "reddit": "https://www.reddit.com"
        }

        for site, url in sites.items():
            if f"open {site}" in query:
                speak(f"Opening {site}, sir...")
                webbrowser.open(url)
                return True

        # --- Wikipedia Search ---
        if "search wikipedia" in query:
            result = searchWikipedia(query)
            speak(result)
            return True

        # --- Time query ---
        if "the time" in query:
            current_time = datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {current_time}")
            return True

        # --- VS Code ---
        if "open code" in query:
            openVSCode()
            return True

        # --- Stop or exit ---
        if "stop" in query or "exit" in query:
            speak("Goodbye, sir!")
            raise SystemExit

        # --- Intent-based actions ---
        intent = detectIntent(query)
        if intent == "play_relaxing_music":
            speak("Playing something relaxing for you.")
            playOnYouTube([
                "lofi chill beats", "relaxing rain sounds", "ambient ocean waves",
                "soft piano music", "nature sounds with birds"
            ])
            return True

        if intent == "give_fun_fact":
            speak("Here's something interesting!")
            playOnYouTube([
                "amazing facts you didn't know", "mind blowing science facts",
                "facts about the universe", "unbelievable history facts"
            ])
            return True

        if intent == "play_motivation":
            speak("Get ready to feel pumped!")
            playOnYouTube([
                "motivational speech by Sandeep Maheshwari",
                "powerful gym motivation",
                "morning motivation",
                "never give up speech",
                "Indian Army motivation"
            ])
            return True

        # --- GPT fallback scenarios ---
        if "motivate me" in query or "inspire me" in query:
            response = ask_gpt("Give me a short motivational speech.")
            speak(response)
            return True

        if "tell me something" in query or "question" in query:
            speak("Sure, ask me anything.")
            from core.listener import takeCommand
            user_query = takeCommand()
            if user_query:
                response = ask_gpt(user_query)
                speak(response)
            else:
                speak("I didn't hear your question.")
            return True

        # --- Default fallback to GPT ---
        logging.info("Falling back to GPT for generic query.")
        response = ask_gpt(query)
        speak(response)
        return True

    except SystemExit:
        raise
    except Exception:
        logging.exception("Error while executing command:")
        return False
