from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Download and cache GPT-2 model and tokenizer
GPT2LMHeadModel.from_pretrained("gpt2")
GPT2Tokenizer.from_pretrained("gpt2")
