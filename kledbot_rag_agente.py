from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from chromadb import HttpClient
from langchain.chains import RetrievalQA
import os

# 🔐 OpenAI Key
os.environ["OPENAI_API_KEY"] = "sk-..."  # <-- Pon aquí tu API key real

# 1. Cliente y embeddings
chroma_client = HttpClient(host="localhost", port=8000)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Carga colecciones
faq = Chroma(client=chroma_client, collection_name="faq", embedding_function=embedding_function)
catalogo = Chroma(client=chroma_client, collection_name="catalogo", embedding_function=embedding_function)

# 3. LLM base
llm = ChatOpenAI(temperature=0)

# 4. Definir funciones para obtener contexto
def obtener_contexto(query):
    contexto = []

    # Buscar en FAQ
    resultados_faq = faq.similarity_search(query, k=2)
    if resultados_faq:
        contexto.append("Información del formulario:\n" + "\n".join([doc.page_content for doc in resultados_faq]))

    # Buscar en catálogo
    resultados_cat = catalogo.similarity_search(query, k=2)
    if resultados_cat:
        contexto.append("Información del catálogo:\n" + "\n".join([str(doc.metadata) for doc in resultados_cat]))

    return "\n\n".join(contexto)

# 5. Función final para consulta RAG
def responder_con_rag(pregunta):
    contexto = obtener_contexto(pregunta)

    if not contexto.strip():
        return "Lo siento, no encontré información relevante en nuestro catálogo o formulario."

    prompt = f"""
Eres un asistente especializado en responder preguntas para clientes de una tienda de equipo de seguridad industrial.

Utiliza la siguiente información extraída del catálogo o formulario para generar una respuesta clara, profesional y útil:

--------------------
{contexto}
--------------------

Ahora responde a esta pregunta del cliente:
{pregunta}
"""

    respuesta = llm.predict(prompt)
    return respuesta

# 6. Ejecutar en consola
if __name__ == "__main__":
    while True:
        pregunta = input("🧤 Pregunta del cliente (o 'salir'): ")
        if pregunta.lower() in ["salir", "exit", "q"]:
            break
        respuesta = responder_con_rag(pregunta)
        print("\n🧠 Respuesta generada:\n", respuesta)
