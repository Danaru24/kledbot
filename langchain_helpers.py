from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generar_preguntas_auxiliares(pregunta_cliente: str, n=2) -> list[str]:
    prompt = f"""
Eres un asistente experto en reformular preguntas para mejorar la búsqueda semántica. 
Dado esta pregunta del cliente: "{pregunta_cliente}", genera {n} preguntas distintas con la misma intención, usando sinónimos, jerga local o estructuras distintas. 
Devuelve solo una lista de preguntas, sin explicaciones, sin enumerar.

Intenta ser concreto y directo, y evita usar palabras como "pregunta", "pregunta del cliente" o "reformulación". Tampoco inicies tu respuesta con "Respuesta:".
No uses comillas ni guiones.
No uses palabras como "pregunta", "pregunta del cliente" o "reformulación".

Pregunta original: "{pregunta_cliente}"
"""
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    variantes = respuesta.choices[0].message.content.strip().split('\n')
    return [v.strip('–-•* ').strip() for v in variantes if v.strip()]
