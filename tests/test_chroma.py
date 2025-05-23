# test_chroma.py

from kledbot.db.chromadb.chroma_setup import chroma_client
from kledbot.db.chromadb.chroma_queries import buscar_productos_similares, buscar_en_formulario

print("Colecciones existentes:", chroma_client.list_collections())

# Obtener las colecciones
collection_catalogo = chroma_client.get_collection("catalogo")
collection_faq = chroma_client.get_collection("faq")

# Contar elementos en cada colección
num_productos = len(collection_catalogo.get()["ids"])
num_preguntas = len(collection_faq.get()["ids"])

print("🧾 Productos en catálogo:", num_productos)
print("📄 Preguntas en FAQ:", num_preguntas)

# Pruebas de búsqueda
print("\n🔍 Búsquedas de prueba:")

query_producto = "guantes"
resultado_producto = buscar_productos_similares(query_producto)
print(f"🛒 Resultado de búsqueda en catálogo ({query_producto}):", resultado_producto or "No encontrado.")

query_faq = "¿Cuál es el horario?"
respuesta_faq = buscar_en_formulario(query_faq)
print(f"❓ Respuesta del formulario ({query_faq}):", respuesta_faq or "No encontrado.")
