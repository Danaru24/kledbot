from flask import Flask, request, jsonify
from kledbot.langchain_chain import responder_mensaje  # ✅ Nuevo import
from kledbot.whatsapp import enviar_mensaje_whatsapp
from config import PUERTO, WEBHOOK_TOKEN
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def recibir_mensaje_whatsapp():
    try:
        data = request.get_json()
        print("🧾 JSON recibido en webhook:", data)

        if not data or "messages" not in data:
            return jsonify({"status": "sin mensajes válidos"}), 200

        mensaje_data = data["messages"][0]
        mensaje = mensaje_data.get("text", "")
        numero = mensaje_data.get("from", "")
        mensaje_id = mensaje_data.get("id", "sin_id")

        print(f"📩 Mensaje recibido de {numero}: {mensaje} (ID: {mensaje_id})")

        # ✅ Corregido: ahora pasamos número y mensaje
        respuesta_bot = responder_mensaje(numero, mensaje)
        print(f"✅ Respuesta generada: {respuesta_bot}")

        numero = numero.replace("@s.whatsapp.net", "")
        enviar_mensaje_whatsapp(numero, respuesta_bot)

        return jsonify({"respuesta": respuesta_bot})

    except Exception as e:
        print("❌ Error interno en webhook:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"🚀 Iniciando servidor Flask en http://0.0.0.0:{PUERTO}")
    app.run(host='0.0.0.0', port=PUERTO)
