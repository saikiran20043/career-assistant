import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from shared_rag import create_retriever


load_dotenv()


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# Shared RAG Retriever
# --------------------------------------------------

retriever = create_retriever()


# --------------------------------------------------
# Skill Gap Prompt
# --------------------------------------------------

skill_gap_prompt = PromptTemplate(
    input_variables=["skills", "target_role", "context"],
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
2. Important skills the user is missing
3. The top 3 skills they should learn first

Keep the answer practical and suitable for a fresher.
"""
)


skill_gap_chain = skill_gap_prompt | llm


# --------------------------------------------------
# Skill Gap Analysis
# --------------------------------------------------

def analyze_skill_gap(skills, target_role):

    search_query = f"""
    Skills, responsibilities and requirements
    for the role of {target_role}.
    """

    retrieved_documents = retriever.invoke(search_query)

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

   

    