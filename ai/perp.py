import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AIML_API_KEY")

if not api_key:
    raise ValueError("⚠️ AIML_API_KEY not found in .env file!")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.aimlapi.com/v1"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Why is the sky blue?"}
    ],
    temperature=0.7,
    max_tokens=128
)

print(response.choices[0].message.content)
