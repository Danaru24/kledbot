import time
from chromadb import HttpClient

while True:
    try:
        client = HttpClient(host="localhost", port=8000)
        client.heartbeat()  # verifica conexión real
        print("✅ ChromaDB está listo.")
        break
    except Exception as e:
        print("⏳ Esperando a que ChromaDB esté disponible...", str(e))
        time.sleep(1)
