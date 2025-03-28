import requests
from flask import request, jsonify

def enviar_mensaje_whatsapp(numero, mensaje):
    url = "http://localhost:3000/sendMessage"  # Endpoint de Baileys
    payload = {
        "number": numero,
        "message": mensaje
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Mensaje enviado a {numero}: {mensaje}")
        else:
            print(f"❌ Error al enviar mensaje: {response.text}")
    except Exception as e:
        print(f"❌ Excepción al enviar mensaje: {e}")


def recibir_mensaje_whatsapp():
    data = request.get_json()

    if not data or "messages" not in data:
        print("⚠️ Webhook recibió un evento sin mensajes válidos:", data)
        return jsonify({"status": "ok"}), 200

    mensaje = data["messages"][0]["text"]
    numero = data["messages"][0]["from"]

    print(f"📩 Mensaje recibido de {numero}: {mensaje}")

    from kledbot.chatbot import obtener_respuesta_kledbot
    respuesta = obtener_respuesta_kledbot(numero, mensaje)
    enviar_mensaje_whatsapp(numero, respuesta)

    return jsonify({"status": "mensaje procesado"}), 200
