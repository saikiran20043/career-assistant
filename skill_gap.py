import os

from dotenv import load_dotenv
from google import genai


# Load API key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Get user information
skills = input(
    "Enter your current skills separated by commas: "
)

target_role = input(
    "Enter your target role: "
)


# Ask Gemini to analyze the skill gap
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"""
You are a career guidance assistant.

Analyze the skill gap between the user's current
skills and their target role.

Current skills:
{skills}

Target role:
{target_role}

Provide:

1. Skills the user already has
2. Important skills they are missing
3. The top 3 skills they should learn first

Keep the answer practical and suitable for a fresher.
"""
)


print("\nSkill Gap Analysis")
print("------------------")

print(response.text)