from chromadb import Client
from chromadb.config import Settings

# Cliente apuntando al directorio de persistencia
chroma_client = Client(Settings(
    persist_directory="./kledbot/db/chromadb_storage"
))

# Comprobación y carga de colecciones
if "catalogo" in chroma_client.list_collections():
    collection_catalogo = chroma_client.get_collection(name="catalogo")
else:
    collection_catalogo = chroma_client.create_collection(name="catalogo")

if "formulario_faq" in chroma_client.list_collections():
    collection_faq = chroma_client.get_collection(name="formulario_faq")
else:
    collection_faq = chroma_client.create_collection(name="formulario_faq")
