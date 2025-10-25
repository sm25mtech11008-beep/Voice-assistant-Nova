# core/gpt_module.py
from transformers import pipeline
import torch
import logging

print("🔁 Initializing GPT module...")

try:
    device = 0 if torch.cuda.is_available() else -1
    generator = pipeline("text-generation", model="gpt2", device=device)
    print(f"✅ GPT module ready (device: {'GPU' if device == 0 else 'CPU'})")
except Exception:
    logging.exception("Failed to initialize GPT generator.")
    generator = None

def ask_gpt(prompt: str) -> str:
    """Generate a text completion using GPT pipeline."""
    if not generator:
        return "GPT model not available."
    try:
        result = generator(prompt, max_length=100, do_sample=True, top_p=0.95, temperature=0.7)
        return result[0]["generated_text"].strip()
    except Exception:
        logging.exception("GPT text generation failed.")
        return "Sorry, I couldn't think of a response right now."
