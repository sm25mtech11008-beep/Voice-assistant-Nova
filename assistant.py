# core/assistant.py

import datetime
from core.speech import speak

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 16:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Nova, sir. Please tell me how may I help you.")
