from app.ai.groq_client import client


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "What is a pharmaceutical manufacturing deviation? Answer in one sentence.",
        }
    ],
)

print(response.choices[0].message.content)