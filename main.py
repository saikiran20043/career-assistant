from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

conversation = []

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    conversation.append({
        "role": "user",
        "parts": [{"text": question}]
    })

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation,
        config={
            "system_instruction": """You are my personal GenAI tutor.
Explain concepts in simple language.
Focus on the big picture before going into details.
Assume I am a beginner."""
        }
    )

    print("\nAI:", response.text)

    conversation.append({
        "role": "model",
        "parts": [{"text": response.text}]
    })