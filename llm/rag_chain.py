import os
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# Load vectorstore from disk (assuming you've already created it via loader.py)
db = FAISS.load_local("llm/vectorstore", HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), allow_dangerous_deserialization=True)

retriever = db.as_retriever()

# Use Groq LLM (LLaMA3)
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

# Optional: custom prompt
template = """You are a compassionate spiritual assistant.
Use the following context to answer the question.
If you don't know the answer, say you don't know.

Context:
{context}

Question:
{question}
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt}
)

def get_similar_scripture(query):
    return qa_chain.run(query)
