import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma


# --------------------------------------------------
# 1. Setup
# --------------------------------------------------

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# 2. Load Career Knowledge
# --------------------------------------------------

documents = []

for filename in os.listdir("Knowledge"):

    if filename.endswith(".txt"):

        file_path = os.path.join(
            "Knowledge",
            filename
        )

        loader = TextLoader(
            file_path,
            encoding="utf-8"
        )

        documents.extend(
            loader.load()
        )


# --------------------------------------------------
# 3. Split Knowledge
# --------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(
    documents
)


# --------------------------------------------------
# 4. Create Vector Store
# --------------------------------------------------

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="resume_analyzer"
)


# --------------------------------------------------
# 5. Create Retriever
# --------------------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 4
    }
)

# --------------------------------------------------
# 6. Resume Analysis Prompt
# --------------------------------------------------

resume_prompt = PromptTemplate(
    input_variables=[
        "resume",
        "target_role",
        "context"
    ],
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
# 6. Analyze Resume
# --------------------------------------------------

def analyze_resume(resume_path, target_role):

    # Load resume PDF
    loader = PyPDFLoader(resume_path)

    resume_documents = loader.load()

    resume = "\n\n".join(
        document.page_content
        for document in resume_documents
    )

    # Retrieve role information
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

    # Analyze resume
    response = resume_chain.invoke({

        "resume": resume,

        "target_role": target_role,

        "context": context
    })

    return response.content


# --------------------------------------------------
# 7. Standalone Testing
# --------------------------------------------------

if __name__ == "__main__":

    resume_path = input(
        "\nEnter the path to your resume PDF: "
    )

    target_role = input(
        "\nEnter your target role: "
    )

    result = analyze_resume(
        resume_path,
        target_role
    )

    print("\n================================")
    print("        RESUME ANALYSIS")
    print("================================")

    print(result)