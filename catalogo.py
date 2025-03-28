# catalogo.py
import pandas as pd
from kledbot.db.chromadb.chroma_queries import collection_catalogo
import os

CATALOGO_PATH = "/root/kledbot/mnt/data/catalogoKled.xlsx"

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

        documentos = []
        metadatos = []

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

        if documentos:
            collection_catalogo.add(documents=documentos, metadatas=metadatos, ids=[f"prod_{i}" for i in range(len(documentos))])
            print(f"✅ Catálogo cargado: {len(documentos)} productos añadidos.")
        else:
            print("❌ No se encontraron productos para cargar.")
    except Exception as e:
        print(f"❌ Error al cargar el catálogo: {e}")

if __name__ == "__main__":
    cargar_catalogo_a_chromadb()
