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
# 6. Interview Prompt
# --------------------------------------------------

interview_prompt = PromptTemplate(
    input_variables=[
        "target_role",
        "context"
    ],
    template="""
You are a career interview preparation assistant.

Help a fresher prepare for the following target role:

Target role:
{target_role}

Use the following career knowledge:

{context}

Create a practical interview preparation plan.

Include:

1. Important technical topics
2. Five technical interview questions
3. Three behavioral interview questions
4. Important areas the candidate should focus on
5. A short preparation strategy

Use the provided career knowledge.
Do not invent specific requirements that are not
supported by the provided information.
"""
)


# --------------------------------------------------
# 7. Create LangChain Chain
# --------------------------------------------------

interview_chain = interview_prompt | llm


# --------------------------------------------------
# 8. Generate Interview Preparation
# --------------------------------------------------

def generate_interview_prep(target_role):

    search_query = f"""
    Interview preparation, skills, responsibilities,
    and important topics for a {target_role}.
    """

    retrieved_documents = retriever.invoke(
        search_query
    )

    context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    response = interview_chain.invoke({
        "target_role": target_role,
        "context": context
    })

    return response.content
# --------------------------------------------------
# 9. Standalone Testing
# --------------------------------------------------

if __name__ == "__main__":

    target_role = input(
        "\nEnter your target role: "
    )

    result = generate_interview_prep(
        target_role
    )

    print("\n================================")
    print("      INTERVIEW PREPARATION")
    print("================================")

    print(result)