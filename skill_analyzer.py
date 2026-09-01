from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

skill = input("Enter a skill: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Analyze my skill in {skill}.",
    config={
        "system_instruction": """You are a career skill analyzer.
Analyze the user's skill.

Return these fields:
- skill
- level
- strengths
- weaknesses
- next_topics""",

        "response_mime_type": "application/json"
    }
)

print("RAW RESPONSE:")
print(response.text)

result = json.loads(response.text)

print("\nPYTHON OBJECT:")
print("\n===== SKILL ANALYSIS =====")

print("Skill:", result["skill"])
print("Level:", result["level"])

print("\nStrengths:")
for item in result["strengths"]:
    print("-", item)

print("\nWeaknesses:")
for item in result["weaknesses"]:
    print("-", item)

print("\nRecommended next topics:")
for item in result["next_topics"]:
    print("-", item)