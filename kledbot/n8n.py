import requests

def enviar_a_n8n(payload: dict):
    url = "http://localhost:5678/webhook/kledbot"  # Cambia al webhook correcto si usas otro
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"❌ Error al enviar a n8n: {e}"
