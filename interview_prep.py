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
# Interview Preparation Prompt
# --------------------------------------------------

interview_prompt = PromptTemplate(
    input_variables=["target_role", "context"],
    template="""
You are a career assistant helping a fresher
prepare for a technical interview.

Target role:
{target_role}

Career knowledge:
{context}

Provide:

1. Important technical topics to study
2. Five technical interview questions
3. Three behavioral interview questions
4. Important areas to focus on
5. A short interview preparation strategy

Keep the answer practical and suitable for a fresher.
"""
)


interview_chain = interview_prompt | llm


# --------------------------------------------------
# Interview Preparation
# --------------------------------------------------

def generate_interview_prep(target_role):

    search_query = f"""
    Interview preparation, skills, responsibilities,
    and important topics for a {target_role}.
    """

    retrieved_documents = retriever.invoke(search_query)

    context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    response = interview_chain.invoke({
        "target_role": target_role,
        "context": context
    })

    return response.content
    