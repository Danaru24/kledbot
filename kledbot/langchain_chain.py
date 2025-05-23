from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from kledbot.db.chromadb.chroma_setup import chroma_vectorstore
from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
load_dotenv()

# Modelo base
llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

# Prompt con historial, contexto y entrada
prompt = PromptTemplate(
    input_variables=["history", "input", "context"],
    template="""
Eres un asistente profesional de una tienda en línea especializada en equipo de seguridad y materiales para la construcción. 
Responde de forma clara, útil y profesional, basándote en el historial y el contexto proporcionado.

Resumen de conversación previa:
{history}

Contexto recuperado:
{context}

Pregunta del cliente:
{input}
"""
)

# Diccionarios globales
memorias_por_usuario = {}
ultimo_mensaje_por_usuario = {}

# Crear nueva memoria resumida
def nueva_memoria():
    return ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000,
        return_messages=True
    )

# Función principal del bot
def responder_mensaje(numero: str, pregunta: str) -> str:
    try:
        ahora = datetime.now()
        limite = timedelta(minutes=15)

        # Reset por tiempo
        if numero in memorias_por_usuario:
            ultima_interaccion = ultimo_mensaje_por_usuario.get(numero, ahora)
            if ahora - ultima_interaccion > limite:
                print(f"🕒 Reiniciando sesión de {numero} por inactividad.")
                del memorias_por_usuario[numero]
                del ultimo_mensaje_por_usuario[numero]

        # Crear memoria si no existe
        if numero not in memorias_por_usuario:
            memorias_por_usuario[numero] = nueva_memoria()

        ultimo_mensaje_por_usuario[numero] = ahora
        memoria = memorias_por_usuario[numero]

        # Obtener contexto
        resultados = chroma_vectorstore.similarity_search(pregunta, k=3)
        documentos_unicos = {doc.page_content: doc for doc in resultados}

        contexto = "\n\n".join([
            f"P: {doc.page_content}\nR: {(
                doc.metadata.get('respuesta', '[sin respuesta]').strip()[2:].strip()
                if doc.metadata.get('respuesta', '').strip().lower().startswith('r:')
                else doc.metadata.get('respuesta')
            )}"
            for doc in documentos_unicos.values()
        ])

        # Cargar historial desde la memoria
        historial = memoria.load_memory_variables({}).get("history", "")

        # Crear prompt final
        prompt_final = prompt.format(
            history=historial,
            input=pregunta,
            context=contexto
        )

        # Obtener respuesta
        respuesta = llm.invoke(prompt_final)

        # Guardar en la memoria
        memoria.save_context(
            inputs={"input": pregunta},
            outputs={"output": respuesta.content}
        )

        return respuesta.content

    except Exception as e:
        return f"Hubo un error al procesar tu solicitud: {str(e)}"
