# 1. Import required libraries
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
# 2. Setup
# --------------------------------------------------

load_dotenv()

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# LangChain Gemini embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# LangChain Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# 3. Load Documents using LangChain
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

            loaded_documents = loader.load()

            documents.extend(loaded_documents)

    return documents


# --------------------------------------------------
# 4. Split Documents using LangChain
# --------------------------------------------------

def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30
    )

    chunks = splitter.split_documents(documents)

    return chunks


# --------------------------------------------------
# 5. Create Chroma Vector Store
# --------------------------------------------------

def create_vectorstore(chunks):

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name="career_knowledge"
    )

    return vectorstore


# --------------------------------------------------
# 6. Rewrite User Question
# --------------------------------------------------

def rewrite_question(
    question,
    conversation_history
):

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in conversation_history
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Rewrite the user's latest question into a standalone question.

Use the conversation history to understand what the user
is referring to.

Return ONLY the rewritten question.

Conversation history:
{history_text}

Latest question:
{question}
"""
    )

    return response.text.strip()


# --------------------------------------------------
# 7. Create Answer Prompt
# --------------------------------------------------

answer_prompt = PromptTemplate(
    input_variables=[
        "history",
        "context",
        "question"
    ],
    template="""
You are a helpful AI assistant.

Use the conversation history and retrieved context
to answer the user's latest question.

Answer using ONLY information supported by the
retrieved context.

If the answer cannot be found in the context, say:

"I don't have enough information in the provided documents."

Do not make up information.

Conversation history:
{history}

Retrieved context:
{context}

Current question:
{question}
"""
)


# --------------------------------------------------
# 8. Create Answer Chain
# --------------------------------------------------

answer_chain = answer_prompt | llm


# --------------------------------------------------
# 9. Retrieve Relevant Documents
# --------------------------------------------------

def retrieve_documents(
    retriever,
    search_question
):

    documents = retriever.invoke(
        search_question
    )

    relevant_chunks = []
    relevant_sources = []

    print("\nRetrieved results:")

    for i, document in enumerate(documents):

        print("\n-----------------------------")

        print(
            "Result:",
            i + 1
        )

        print(
            "Source:",
            document.metadata.get(
                "source",
                "Unknown"
            )
        )

        print(
            "Chunk:",
            document.page_content
        )

        relevant_chunks.append(
            document.page_content
        )

        relevant_sources.append(
            document.metadata.get(
                "source",
                "Unknown"
            )
        )

    return relevant_chunks, relevant_sources


# --------------------------------------------------
# 10. Generate Final Answer
# --------------------------------------------------

def generate_answer(
    question,
    context,
    conversation_history
):

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in conversation_history
    )

    response = answer_chain.invoke({
        "history": history_text,
        "context": context,
        "question": question
    })

    return response.content


# --------------------------------------------------
# 11. Prepare Knowledge Base
# --------------------------------------------------

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
    "Knowledge base successfully created."
)


# --------------------------------------------------
# 12. Create Retriever
# --------------------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)


# --------------------------------------------------
# 13. Conversation History
# --------------------------------------------------

conversation_history = []


# --------------------------------------------------
# 14. Chatbot Loop
# --------------------------------------------------

while True:

    question = input(
        "\nAsk a question (type 'exit' to quit): "
    )

    # Stop chatbot
    if question.lower() == "exit":
        break


    # --------------------------------------------------
    # Store user question
    # --------------------------------------------------

    conversation_history.append({
        "role": "user",
        "content": question
    })


    # --------------------------------------------------
    # Rewrite question
    # --------------------------------------------------

    search_question = rewrite_question(
        question,
        conversation_history
    )

    print(
        "\nSearch question:",
        search_question
    )


    # --------------------------------------------------
    # Retrieve relevant documents
    # --------------------------------------------------

    relevant_chunks, sources = retrieve_documents(
        retriever,
        search_question
    )


    # --------------------------------------------------
    # Handle no retrieved documents
    # --------------------------------------------------

    if not relevant_chunks:

        answer = (
            "I don't have enough information "
            "in the provided documents."
        )

        print("\nAnswer:")
        print(answer)

        print("\nSources:")
        print("No relevant sources found.")

        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        continue


    # --------------------------------------------------
    # Combine retrieved chunks
    # --------------------------------------------------

    context = "\n\n".join(
        relevant_chunks
    )


    # --------------------------------------------------
    # Generate answer
    # --------------------------------------------------

    answer = generate_answer(
        question,
        context,
        conversation_history
    )


    # --------------------------------------------------
    # Display answer
    # --------------------------------------------------

    print("\nAnswer:")
    print(answer)


    # --------------------------------------------------
    # Display sources
    # --------------------------------------------------

    print("\nSources:")

    for source in sorted(set(sources)):
        print("-", source)


    # --------------------------------------------------
    # Store assistant answer
    # --------------------------------------------------

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })