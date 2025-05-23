from chromadb import HttpClient
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Cliente de ChromaDB local
chroma_client = HttpClient(host="localhost", port=8000)

# Embeddings compatibles con colección "faq" (dimensión 384)
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Vectorstore conectado a la colección correcta
chroma_vectorstore = Chroma(
    client=chroma_client,
    collection_name="faq",
    embedding_function=embedding_function
)
