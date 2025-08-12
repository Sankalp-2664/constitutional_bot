import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API Key not found. Please set it in your .env file.")

# Path to FAISS index - Updated to match build_faiss.py
faiss_path = "vector_store/faiss_index_constitution"
if not os.path.exists(f"{faiss_path}/index.faiss"):
    raise FileNotFoundError(f"FAISS index not found at {faiss_path}. Please build the index first.")

# Load vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# LLM model
llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)

# Prompt for constitutional expertise
prompt_template = """
You are a constitutional expert specializing in the Constitution of India.
Provide accurate, clear, and unbiased legal explanations.

User Question:
{question}

Relevant Context from the Constitution:
{context}

Instructions:
- Base your answer strictly on the given context and your knowledge of the Constitution.
- Cite Article numbers and headings when possible.
- Stay neutral, factual, and avoid personal opinions.
- If the context is insufficient, say so and provide general constitutional principles.

Now provide the answer:
"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Retrieval-based QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
    chain_type="stuff"
)

def ask_samvidhan(question: str) -> str:
    """Answer queries about the Constitution of India with sources."""
    result = qa_chain({"query": question})
    answer = result.get("result", "Sorry, I couldn't find an answer.")
    sources = result.get("source_documents", [])

    if sources:
        answer += "\n\n**Sources:**"
        seen = set()
        for doc in sources:
            src = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "")
            src_info = f"{src} (Page {page})" if page else src
            if src_info not in seen:
                seen.add(src_info)
                answer += f"\n- {src_info}"

    return answer

# Add alias for backward compatibility if needed
ask_samvidhan_chatbot = ask_samvidhan

if __name__ == "__main__":
    while True:
        query = input("Ask me about the Constitution of India: ")
        if query.lower() == "exit":
            break
        print("📜:", ask_samvidhan(query))