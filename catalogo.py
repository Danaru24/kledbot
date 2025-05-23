# catalogo.py
import pandas as pd
from kledbot.db.chromadb.chroma_setup import chroma_client
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

CATALOGO_PATH = "/root/kledbot/mnt/data/catalogoKled.xlsx"
CHROMA_BATCH_SIZE = 20         # Lote para añadir a chromadb
EMBEDDING_BATCH_SIZE = 8       # Lote para generar embeddings (más pequeño = menos RAM)

def cargar_catalogo_a_chromadb():
    print("📦 Cargando catálogo...")

    if not os.path.exists(CATALOGO_PATH):
        print(f"❌ El archivo {CATALOGO_PATH} no fue encontrado.")
        return

    try:
        df = pd.read_excel(CATALOGO_PATH)
        df.columns = df.columns.str.strip().str.lower()
        print("📊 Columnas encontradas:", df.columns)

        required_columns = ["nombre", "precio", "categoria", "stock", "descripcion", "url"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Columna faltante: {col}")

        collection_catalogo = chroma_client.get_or_create_collection(name="catalogo")

        documentos = []
        metadatos = []
        ids = []

        for i, row in df.iterrows():
            texto = f"{row['nombre']} - {row['descripcion']}"
            documentos.append(texto)
            metadatos.append({
                "nombre": row["nombre"],
                "precio": row["precio"],
                "categoria": row["categoria"],
                "stock": row["stock"],
                "url": row["url"]
            })
            ids.append(f"prod_{i}")

            # Cargar a ChromaDB en lotes
            if len(documentos) == CHROMA_BATCH_SIZE:
                embeddings = model.encode(documentos, batch_size=EMBEDDING_BATCH_SIZE, show_progress_bar=False).tolist()
                collection_catalogo.add(
                    documents=documentos,
                    metadatas=metadatos,
                    ids=ids,
                    embeddings=embeddings
                )
                documentos, metadatos, ids = [], [], []

        # Cargar el último lote
        if documentos:
            embeddings = model.encode(documentos, batch_size=EMBEDDING_BATCH_SIZE, show_progress_bar=False).tolist()
            collection_catalogo.add(
                documents=documentos,
                metadatas=metadatos,
                ids=ids,
                embeddings=embeddings
            )

        print(f"✅ Catálogo cargado: {len(df)} productos añadidos.")
    except Exception as e:
        print(f"❌ Error al cargar el catálogo: {e}")

if __name__ == "__main__":
    cargar_catalogo_a_chromadb()
