# core/wake_listener.py

import speech_recognition as sr

def listen_for_wake_word(wake_word="hey nova"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        text = recognizer.recognize_google(audio).lower()
        print("Heard:", text)
        return wake_word in text
    except sr.UnknownValueError:
        return False
    except sr.RequestError:
        return False
