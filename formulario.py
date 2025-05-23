# formulario.py
from kledbot.db.chromadb.chroma_setup import chroma_client
from sentence_transformers import SentenceTransformer
import os

FORMULARIO_PATH = "/root/kledbot/mnt/data/Formulario_Informacion.txt"

# Inicializar modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_textos(textos):
    return model.encode(textos).tolist()

def cargar_formulario_a_chromadb():
    print("📄 Cargando formulario de información...")

    if not os.path.exists(FORMULARIO_PATH):
        print(f"❌ El archivo {FORMULARIO_PATH} no fue encontrado.")
        return

    collection_faq = chroma_client.get_or_create_collection(name="faq")

    try:
        docs = collection_faq.get()
        if docs and docs["ids"]:
            collection_faq.delete(ids=docs["ids"])
            print("🧹 Datos anteriores eliminados.")
    except Exception as e:
        print(f"⚠️ No se pudo limpiar la colección: {e}")

    with open(FORMULARIO_PATH, "r", encoding="utf-8") as file:
        lines = file.readlines()

    seccion = ""
    pregunta = ""
    respuesta = ""
    documentos = []
    metadatos = []

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#") or "Formulario de Información" in line:
            continue
        if line[0].isdigit() and line[1] == ".":
            seccion = line.strip()
            continue
        if line.startswith("P:"):
            pregunta = line[2:].strip()
        elif line.lower().startswith("r:") or line.lower().startswith("respuesta:"):
            if line.lower().startswith("respuesta:"):
                respuesta = line[len("respuesta:"):].strip()
            else:
                respuesta = line[2:].strip()
            documentos.append(pregunta)
            metadatos.append({"seccion": seccion, "respuesta": respuesta})

    #print(f"📄 Se encontraron {documentos} preguntas en el formulario.")
    #imprimir pregunta y respuesta
    
    """ 
    for i, doc in enumerate(documentos):
        print(f"Pregunta {i+1}: {doc}")
        print(f"Respuesta: {metadatos[i]['respuesta']}")
        print("-" * 40)
    """

    if documentos:
        embeddings = embed_textos(documentos)

        collection_faq.add(
            documents=documentos,
            metadatas=metadatos,
            ids=[f"faq_{i}" for i in range(len(documentos))],
            embeddings=embeddings  # ✅ Embeddings personalizados
        )
        print(f"✅ Formulario cargado: {len(documentos)} preguntas añadidas.")
    else:
        print("❌ No se encontraron preguntas válidas.")

if __name__ == "__main__":
    cargar_formulario_a_chromadb()
