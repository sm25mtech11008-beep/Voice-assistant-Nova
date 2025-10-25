import openai

openai.api_key = "sk-proj-..."  # Your real API key

def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"GPT Error: {str(e)}"

print(ask_gpt("What is the capital of India?"))
