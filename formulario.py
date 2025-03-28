# formulario.py
from kledbot.db.chromadb.chroma_setup import chroma_client
import os

FORMULARIO_PATH = "/root/kledbot/mnt/data/Formulario_Informacion.txt"

def cargar_formulario_a_chromadb():
    print("📄 Cargando formulario de información...")

    if not os.path.exists(FORMULARIO_PATH):
        print(f"❌ El archivo {FORMULARIO_PATH} no fue encontrado.")
        return

    # Obtener o crear colección
    collection_faq = chroma_client.get_or_create_collection(name="faq")

    # Eliminar datos anteriores
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

        if not line:
            continue
        if line.startswith("#") or "Formulario de Información" in line:
            continue
        if line[0].isdigit() and line[1] == ".":
            seccion = line.strip()
            continue
        if line.startswith("P:"):
            pregunta = line[2:].strip()
        elif line.startswith("R:"):
            respuesta = line[2:].strip()
            documentos.append(pregunta)
            metadatos.append({"seccion": seccion, "respuesta": respuesta})

    if documentos:
        collection_faq.add(
            documents=documentos,
            metadatas=metadatos,
            ids=[f"faq_{i}" for i in range(len(documentos))]
        )
        print(f"✅ Formulario cargado: {len(documentos)} preguntas añadidas.")
    else:
        print("❌ No se encontraron preguntas válidas.")

if __name__ == "__main__":
    cargar_formulario_a_chromadb()
