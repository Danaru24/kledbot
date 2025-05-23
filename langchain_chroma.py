from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from chromadb import HttpClient

# Cliente de ChromaDB (ya lo tienes corriendo en localhost:8000)
chroma_client = HttpClient(host="localhost", port=8000)

# Embeddings que usará LangChain para comparar consultas
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Colecciones existentes: 'catalogo' y 'faq'
catalogo_vectorstore = Chroma(
    client=chroma_client,
    collection_name="catalogo",
    embedding_function=embedding_function
)

faq_vectorstore = Chroma(
    client=chroma_client,
    collection_name="faq",
    embedding_function=embedding_function
)


if __name__ == "__main__":
    query = "¿Cuál es el horario?"
    docs = faq_vectorstore.similarity_search(query, k=1)
    print("📄 Respuesta más cercana en FAQ:")
    for d in docs:
        print("-", d.page_content)

    print("\n🛒 Producto buscado: guantes")
    productos = catalogo_vectorstore.similarity_search("guantes", k=1)
    for p in productos:
        print("-", p.metadata)
