from kledbot.db.chromadb.chroma_setup import chroma_client

def mostrar_contenido_de_coleccion(nombre):
    print(f"\n📂 Colección: {nombre}")
    collection = chroma_client.get_collection(name=nombre)

    resultados = collection.get(include=["documents", "metadatas"])
    documentos = resultados["documents"]
    metadatos = resultados["metadatas"]

    print(f"🔢 Total de entradas: {len(documentos)}")

    for i, (doc, meta) in enumerate(zip(documentos, metadatos), start=1):
        print(f"\n🔹 Entrada {i}:")
        print(f"📄 Document: {doc}")
        print(f"🧾 Metadata: {meta}")

if __name__ == "__main__":
    mostrar_contenido_de_coleccion("faq")
    mostrar_contenido_de_coleccion("catalogo")
