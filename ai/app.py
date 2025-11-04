from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "sk-"

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain why the sky is blue in one short sentence."}
    ]
)

print("Status: ✅")
print("Reply:", response.choices[0].message.content)
