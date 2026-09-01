import os

from dotenv import load_dotenv
from google import genai

from langchain_community.document_loaders import TextLoader
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

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

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
# 3. Split Documents
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
    collection_name="career_assistant"
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
# 6. Get User Profile
# --------------------------------------------------

skills = input(
    "\nEnter your current skills separated by commas: "
)

target_role = input(
    "Enter your target role: "
)


# --------------------------------------------------
# 7. Retrieve Career Requirements
# --------------------------------------------------

search_query = f"""
Skills required for {target_role}
and preparation needed for this role.
"""

retrieved_documents = retriever.invoke(
    search_query
)


context = "\n\n".join(
    document.page_content
    for document in retrieved_documents
)


# --------------------------------------------------
# 8. Create Skill Gap Prompt
# --------------------------------------------------

skill_gap_prompt = PromptTemplate(
    input_variables=[
        "skills",
        "target_role",
        "context"
    ],
    template="""
You are a career guidance assistant.

Analyze the user's current skills against
the requirements for their target role.

Current skills:
{skills}

Target role:
{target_role}

Career knowledge:
{context}

Provide:

1. Skills the user already has
2. Important skills they are missing
3. Top 3 skills they should learn first
4. A short recommended learning direction

Use the provided career knowledge.
Do not invent requirements that are not supported
by the knowledge provided.
"""
)


# --------------------------------------------------
# 9. Create LangChain Chain
# --------------------------------------------------

skill_gap_chain = skill_gap_prompt | llm


# --------------------------------------------------
# 10. Generate Analysis
# --------------------------------------------------

response = skill_gap_chain.invoke({
    "skills": skills,
    "target_role": target_role,
    "context": context
})


# --------------------------------------------------
# 11. Display Result
# --------------------------------------------------

print("\n================================")
print("       SKILL GAP ANALYSIS")
print("================================")

print(response.content)