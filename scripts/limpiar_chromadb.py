# limpiar_chromadb.py
from kledbot.db.chromadb.chroma_setup import chroma_client

def limpiar_coleccion(nombre):
    try:
        collection = chroma_client.get_or_create_collection(name=nombre)
        documentos = collection.get()
        if documentos and documentos["ids"]:
            collection.delete(ids=documentos["ids"])
            print(f"🧹 Colección '{nombre}' limpiada: {len(documentos['ids'])} documentos eliminados.")
        else:
            print(f"ℹ️ Colección '{nombre}' ya estaba vacía.")
    except Exception as e:
        print(f"❌ Error al limpiar colección '{nombre}': {e}")

if __name__ == "__main__":
    print("🧽 Limpiando colecciones ChromaDB...\n")
    limpiar_coleccion("faq")
    limpiar_coleccion("catalogo")
    print("\n✅ Proceso completado.")
