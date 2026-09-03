import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# --------------------------------------------------
# 1. Setup
# --------------------------------------------------

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# 2. Load Career Knowledge
# --------------------------------------------------

def load_documents(folder_path="Knowledge"):

    documents = []

    for filename in os.listdir(folder_path):

        if filename.endswith(".txt"):

            file_path = os.path.join(
                folder_path,
                filename
            )

            loader = TextLoader(
                file_path,
                encoding="utf-8"
            )

            documents.extend(
                loader.load()
            )

    return documents


# --------------------------------------------------
# 3. Split Documents
# --------------------------------------------------

def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30
    )

    return splitter.split_documents(
        documents
    )


# --------------------------------------------------
# 4. Create Vector Store
# --------------------------------------------------

def create_vectorstore(chunks):

    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name="career_knowledge"
    )


# --------------------------------------------------
# 5. Create Shared Retriever
# --------------------------------------------------

def create_retriever():

    documents = load_documents()

    print(
        "Number of documents:",
        len(documents)
    )

    chunks = chunk_documents(
        documents
    )

    print(
        "Number of chunks:",
        len(chunks)
    )

    vectorstore = create_vectorstore(
        chunks
    )

    print(
        "Shared knowledge base successfully created."
    )

    return vectorstore.as_retriever(
        search_kwargs={
            "k": 3
        }
    )
# --------------------------------------------------
# 6. Test Shared Retriever
# --------------------------------------------------

if __name__ == "__main__":

    retriever = create_retriever()

    results = retriever.invoke(
        "skills required for a Generative AI Engineer"
    )

    print("\nRetrieved Documents:")

    for document in results:

        print("\n-----------------------------")

        print(document.page_content)

        print(
            "Source:",
            document.metadata.get(
                "source",
                "Unknown"
            )
        )