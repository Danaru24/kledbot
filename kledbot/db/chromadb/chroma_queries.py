# chroma_queries.py
from kledbot.db.chromadb.chroma_setup import chroma_client

# ✅ Estos comandos aseguran que las colecciones existan (si no existen, las crean)
collection_catalogo = chroma_client.get_or_create_collection(name="catalogo")
collection_faq = chroma_client.get_or_create_collection(name="faq")

def buscar_productos_similares(query):
    resultados = collection_catalogo.query(
        query_texts=[query],
        n_results=1
    )
    if resultados["metadatas"]:
        return resultados["metadatas"][0][0]
    return None

def buscar_en_formulario(query):
    resultados = collection_faq.query(
        query_texts=[query],
        n_results=1
    )
    if resultados["metadatas"]:
        return resultados["metadatas"][0][0]["respuesta"]
    return None
