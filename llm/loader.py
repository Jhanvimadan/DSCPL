import os
from langchain.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

data_path = "data/devotions"
persist_path = "llm/vectorstore"

# Load all text files
documents = []
for filename in os.listdir(data_path):
    if filename.endswith(".txt"):
        loader = TextLoader(os.path.join(data_path, filename), encoding="utf-8")
        documents.extend(loader.load())

# Split into chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Use HuggingFace embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS index
db = FAISS.from_documents(docs, embedding_model)

# Save vectorstore
db.save_local(persist_path)
print(f"✅ Vectorstore saved to {persist_path}")
for filename in os.listdir(data_path):
    if filename.endswith(".txt"):
        print(f"Loading {filename}...")
        try:
            loader = TextLoader(os.path.join(data_path, filename))
            documents.extend(loader.load())
        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")
