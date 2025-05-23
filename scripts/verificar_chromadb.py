from kledbot.db.chromadb.chroma_setup import chroma_vectorstore

docs = chroma_vectorstore.similarity_search("¿Cuál es el horario de atención?", k=5)

print("Documentos recuperados:")
for i, doc in enumerate(docs):
    print(f"\n🔹 Documento {i+1}:\n{doc.page_content}")
