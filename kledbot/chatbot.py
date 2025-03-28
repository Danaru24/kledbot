from openai import OpenAI
from kledbot.db.chromadb.chroma_setup import chroma_client
from kledbot.db.chromadb.chroma_queries import collection_faq, collection_catalogo
from kledbot.utils import limpiar_texto

import os

from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def buscar_contexto_en_chromadb(pregunta):
    """Busca en FAQ y catálogo y devuelve contexto combinado"""
    contexto = []

    # Buscar en FAQ
    faq_results = collection_faq.query(query_texts=[pregunta], n_results=2)
    for doc, meta in zip(faq_results["documents"][0], faq_results["metadatas"][0]):
        contexto.append(f"Q: {doc}\nA: {meta['respuesta']}")

    # Buscar en catálogo
    cat_results = collection_catalogo.query(query_texts=[pregunta], n_results=1)
    for doc, meta in zip(cat_results["documents"][0], cat_results["metadatas"][0]):
        contexto.append(f"Producto: {meta['nombre']}\nPrecio: {meta['precio']}")

    return "\n\n".join(contexto).strip()

def obtener_respuesta_kledbot(numero_usuario, mensaje):
    pregunta = limpiar_texto(mensaje)
    contexto = buscar_contexto_en_chromadb(pregunta)
    print("contexto: ", contexto)
    if contexto:
        prompt = (
            f"Utiliza la siguiente información para responder como asistente de la tienda KLED:\n\n"
            f"{contexto}\n\n"
            f"Usuario: {pregunta}\n"
            f"Asistente:"
        )
    else:
        prompt = (
            f"Eres un asistente de la tienda KLED. Responde al usuario de forma amigable.\n"
            f"Usuario: {pregunta}\n"
            f"Asistente:"
        )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()
