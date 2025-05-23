from openai import OpenAI
from kledbot.db.chromadb.chroma_setup import chroma_client
from kledbot.db.chromadb.chroma_queries import collection_faq, collection_catalogo
from kledbot.utils import limpiar_texto
from collections import defaultdict

import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

SIMILARITY_THRESHOLD = 0.4
KEYWORDS_SECCION1 = ["kled", "tienda", "productos", "tipo de tienda", "qué venden", "construcción", "equipo de seguridad"]

def pertenece_a_tema_general(pregunta):
    pregunta_lower = pregunta.lower()
    return any(keyword in pregunta_lower for keyword in KEYWORDS_SECCION1)

def buscar_contexto_en_chromadb(pregunta):
    contexto_secciones = defaultdict(list)
    contexto = []

    # Verificamos si debemos priorizar la sección 1
    prioridad_seccion1 = pertenece_a_tema_general(pregunta)

    # --- Buscar en FAQ ---
    faq_resultados = collection_faq.query(
        query_texts=[pregunta],
        n_results=10,
        include=["documents", "metadatas", "distances"]
    )

    faq_docs = faq_resultados["documents"][0]
    faq_metas = faq_resultados["metadatas"][0]
    faq_scores = faq_resultados["distances"][0]

    for doc, meta, score in zip(faq_docs, faq_metas, faq_scores):
        seccion = meta.get("seccion", "Sección desconocida")
        if score < SIMILARITY_THRESHOLD:
            if prioridad_seccion1 and seccion.startswith("1. "):  # Forzamos incluir sección 1 si aplica
                print(f"✅ [PRIORIDAD] FAQ sección 1 incluido (score={score:.2f}): {doc}")
                contexto_secciones[seccion].append(f"Q: {doc}\nA: {meta['respuesta']}")
            else:
                print(f"✅ FAQ incluido (score={score:.2f}): {doc}")
                contexto_secciones[seccion].append(f"Q: {doc}\nA: {meta['respuesta']}")
        else:
            print(f"❌ FAQ descartado por baja similitud (score={score:.2f}): {doc}")

    # --- Buscar en Catálogo ---
    cat_resultados = collection_catalogo.query(
        query_texts=[pregunta],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    cat_docs = cat_resultados["documents"][0]
    cat_metas = cat_resultados["metadatas"][0]
    cat_scores = cat_resultados["distances"][0]

    for doc, meta, score in zip(cat_docs, cat_metas, cat_scores):
        if score < SIMILARITY_THRESHOLD:
            print(f"✅ Producto incluido (score={score:.2f}): {meta['nombre']}")
            contexto_secciones["Catálogo de Productos"].append(
                f"Producto: {meta['nombre']}\nPrecio: {meta['precio']}"
            )
        else:
            print(f"❌ Producto descartado por baja similitud (score={score:.2f}): {meta['nombre']}")

    # --- Construir contexto final agrupado por sección ---
    for seccion, contenidos in contexto_secciones.items():
        contexto.append(f"[{seccion}]\n" + "\n".join(contenidos))

    contexto_final = "\n\n".join(contexto).strip()

    print("\n🧠 Contexto final enviado a ChatGPT:\n", contexto_final if contexto_final else "[Sin contexto útil]")

    return contexto_final


def obtener_respuesta_kledbot(numero_usuario, mensaje):
    pregunta = limpiar_texto(mensaje)
    contexto = buscar_contexto_en_chromadb(pregunta)

    if contexto:
        prompt = (
            f"Utiliza la siguiente información para responder como asistente de la tienda KLED. "
            f"Si la información no es suficiente, responde con cortesía pero admite que no sabes la respuesta.\n\n"
            f"{contexto}\n\n"
            f"Usuario: {pregunta}\n"
            f"Asistente:"
        )
    else:
        prompt = (
            f"Eres un asistente de la tienda KLED. Si no sabes la respuesta o no tienes información suficiente, "
            f"indícalo amablemente. No inventes información.\n\n"
            f"Usuario: {pregunta}\n"
            f"Asistente:"
        )


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()
