# core/gpt_response.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import logging

print("🔁 Loading offline GPT-2 model...")
try:
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(DEVICE)
    print(f"✅ GPT-2 loaded on {DEVICE}")
except Exception:
    logging.exception("Failed to load GPT-2 model.")
    tokenizer = model = None
    DEVICE = "cpu"

def get_offline_reply(prompt: str, max_length: int = 100) -> str:
    """Generate a short text completion from local GPT-2."""
    if not model or not tokenizer:
        return "Offline model not available."

    try:
        with torch.no_grad():
            inputs = tokenizer.encode(prompt, return_tensors="pt").to(DEVICE)
            outputs = model.generate(
                inputs,
                max_length=max_length,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id,
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()
    except Exception:
        logging.exception("Offline GPT generation failed.")
        return "Sorry, I couldn't process that right now."
