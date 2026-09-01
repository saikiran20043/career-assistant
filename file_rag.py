# 1. Import required libraries
import chromadb
from google import genai
from dotenv import load_dotenv
import os


# 2. Load API key and create Gemini client
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# 3. Create ChromaDB client and collection
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="file_knowledge"
)
# 4. Load the text file
with open("knowledge/career.txt", "r", encoding="utf-8") as file:
    document = file.read()


# 5. Set chunk size and overlap
chunk_size = 150
overlap = 30

chunks = []


# 6. Split the document into overlapping chunks
start = 0

while start < len(document):

    chunk = document[start:start + chunk_size]

    chunks.append(chunk)

    start += chunk_size - overlap


# 7. Check how many chunks were created
print("Number of chunks:", len(chunks))
# 8. Create an embedding for every chunk
embeddings = []

for chunk in chunks:

    embedding_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )

    embeddings.append(
        embedding_response.embeddings[0].values
    )

print("Number of embeddings:", len(embeddings))
# 9. Create an ID for each chunk
ids = []

for i in range(len(chunks)):
    ids.append(f"chunk_{i}")


# 10. Store chunks and embeddings in ChromaDB
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings
)

print("Chunks successfully stored in ChromaDB")