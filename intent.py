# core/intent.py
import re

def detectIntent(query):
    """Detect user intent based on simple keyword matching."""
    query = query.lower()

    patterns = {
        "play_relaxing_music": ["tired", "sleepy", "low energy", "no mood", "relax"],
        "give_fun_fact": ["learn", "teach", "interesting", "something new", "fact"],
        "play_motivation": ["motivate", "inspire", "encourage", "motivation"],
    }

    for intent, keywords in patterns.items():
        if any(re.search(rf"\b{kw}\b", query) for kw in keywords):
            return intent

    return "unknown"
