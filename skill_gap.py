import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from shared_rag import create_retriever

# --------------------------------------------------
# 1. Setup
# --------------------------------------------------

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)
retriever = create_retriever()


# --------------------------------------------------
# 2. Create Prompt
# --------------------------------------------------

skill_gap_prompt = PromptTemplate(
    input_variables=[
    "skills",
    "target_role",
    "context"
],
    template="""
You are a career guidance assistant.

Analyze the skill gap between the user's current
skills and their target role.

Current skills:
{skills}

Target role:
{target_role}

Career knowledge:
{context}

Provide:

1. Skills the user already has
2. Important skills they are missing
3. The top 3 skills they should learn first

Base your analysis on the provided career knowledge.

Keep the answer practical and suitable for a fresher.
""")

# --------------------------------------------------
# 3. Create Chain
# --------------------------------------------------

skill_gap_chain = skill_gap_prompt | llm


# --------------------------------------------------
# 4. Skill Gap Function
# --------------------------------------------------

def analyze_skill_gap(skills, target_role):

    search_query = f"""
    Skills, responsibilities and requirements
    for the role of {target_role}.
    """

    retrieved_documents = retriever.invoke(
        search_query
    )

    context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    response = skill_gap_chain.invoke({
        "skills": skills,
        "target_role": target_role,
        "context": context
    })

    return response.content

# --------------------------------------------------
# 5. Test the Function
# --------------------------------------------------

if __name__ == "__main__":

    skills = input(
        "Enter your current skills separated by commas: "
    )

    target_role = input(
        "Enter your target role: "
    )

    result = analyze_skill_gap(
        skills,
        target_role
    )

    print("\nSkill Gap Analysis")
    print("------------------")

    print(result)