import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
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
# Resume Analysis Prompt
# --------------------------------------------------

resume_prompt = PromptTemplate(
    input_variables=["resume", "target_role", "context"],
    template="""
You are a career assistant helping a fresher
evaluate their resume.

Analyze the resume against the target role.

Target role:
{target_role}

Resume:
{resume}

Career knowledge:
{context}

Provide:

1. Overall role alignment
2. Strong skills and relevant experience
3. Missing or weak skills
4. Projects or experience that should be highlighted
5. Top 5 improvements to make the resume stronger

Base your analysis on the provided career knowledge.
Be practical and concise.
"""
)


resume_chain = resume_prompt | llm


# --------------------------------------------------
# Resume Analysis
# --------------------------------------------------

def analyze_resume(resume_path, target_role):

    loader = PyPDFLoader(resume_path)

    resume_documents = loader.load()

    resume = "\n\n".join(
        document.page_content
        for document in resume_documents
    )

    search_query = f"""
    Skills, responsibilities and requirements
    for the role of {target_role}.
    """

    retrieved_documents = retriever.invoke(search_query)

    context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    response = resume_chain.invoke({
        "resume": resume,
        "target_role": target_role,
        "context": context
    })

    # Convert Gemini/LangChain response into plain text
    return response.content