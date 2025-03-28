# kledbot/utils.py

import re

def limpiar_texto(texto):
    """
    Limpia y normaliza el texto para facilitar la búsqueda en ChromaDB.
    """
    texto = texto.lower()
    texto = re.sub(r"[^a-zA-Z0-9áéíóúñü\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()
