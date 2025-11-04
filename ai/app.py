from openai import OpenAI
import os

# Either export the key in your terminal:
# setx OPENAI_API_KEY "sk-..."
# or paste it directly here for testing
os.environ["OPENAI_API_KEY"] = "sk-"
# proj-ak_Z5QaI8v-RgmznLfr7tixQO5uuLWliRKrkptkIqTh4edYgYluDa9K8ZrOrvijz99b_b80KDyT3BlbkFJHP5EIPPasN50XAa7O4IlTdqybOveZnr-2PrtKIPxQN9A1Tjna9D5S0C3vqNiIUMDQY1umGqDMA
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
