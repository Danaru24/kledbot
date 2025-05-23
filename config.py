# config.py
from dotenv import load_dotenv
load_dotenv()

# API de OpenAI
OPENAI_API_KEY = "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"

# Puerto del servidor Flask
PUERTO = 5000

# Token para asegurar el webhook (puede usarse en n8n o validaciones futuras)
WEBHOOK_TOKEN = "kledbot_token"

# Ruta de persistencia para ChromaDB
CHROMA_DB_PATH = "/root/kledbot/kledbot/db/chromadb_storage"

# Ruta del catálogo y formulario
RUTA_CATALOGO = "/root/kledbot/mnt/data/catalogoKled.xlsx"
RUTA_FORMULARIO = "/root/kledbot/mnt/data/Formulario_Informacion.txt"
