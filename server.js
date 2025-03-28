const express = require("express");
const {
    default: makeWASocket,
    useMultiFileAuthState,
    fetchLatestBaileysVersion,
    makeInMemoryStore,
    DisconnectReason,
} = require("@whiskeysockets/baileys");

const P = require("pino");
const fs = require("fs");
const path = require("path");
const axios = require("axios");

global.crypto = require("crypto");

const app = express();
app.use(express.json());

const authDir = "./baileys_auth";

if (!fs.existsSync(authDir)) {
    fs.mkdirSync(authDir, { recursive: true });
}

const store = makeInMemoryStore({
    logger: P({ level: "silent", stream: "store" }),
});

let sock;
const processedMessages = new Set();  // ✅ Mensajes ya procesados

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState(authDir);
    const { version } = await fetchLatestBaileysVersion();

    sock = makeWASocket({
        version,
        auth: state,
        logger: P({ level: "silent" }),
        printQRInTerminal: true,
        syncFullHistory: false,
    });

    store.bind(sock.ev);
    sock.ev.on("creds.update", saveCreds);

    sock.ev.on("connection.update", ({ connection, lastDisconnect }) => {
        if (connection === "close") {
            const shouldReconnect = (lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut);
            console.log("❌ Conexión cerrada. Reintentando:", shouldReconnect);
            if (shouldReconnect) startBot();
        } else if (connection === "open") {
            console.log("✅ Conectado a WhatsApp correctamente.");
        }
    });

    sock.ev.on("messages.upsert", async ({ messages, type }) => {
    if (type !== "notify") return;
    const msg = messages[0];
    if (!msg.message || msg.key.fromMe) return;

    const mensajeTexto = msg.message.conversation || msg.message.extendedTextMessage?.text;
    const numero = msg.key.remoteJid;

    console.log(`📩 Mensaje recibido de ${numero}: ${mensajeTexto}`);

    const axios = require("axios");
    try {
        const response = await axios.post("http://localhost:5000/webhook", {
            messages: [{ text: mensajeTexto, from: numero }],
        });
        const respuestaBot = response.data.respuesta || "🤖 Procesado.";
        
        const jid = numero.endsWith("@s.whatsapp.net") ? numero : `${numero}@s.whatsapp.net`;
        await sock.sendMessage(jid, { text: respuestaBot });
        console.log(`✅ Mensaje enviado a ${jid}: ${respuestaBot}`);
    } catch (e) {
        console.error("❌ Error enviando al webhook:", e.message);
    }
});

  
  
}

app.post("/sendMessage", async (req, res) => {
    const { number, message } = req.body;
    if (!number || !message) {
        return res.status(400).json({ error: "Número y mensaje son requeridos." });
    }

    try {
        await sock.sendMessage(number , { text: message });
        console.log(`✅ Mensaje enviado a ${number}: ${message}`);
        res.json({ status: "enviado" });
    } catch (e) {
        console.error("❌ Error al enviar mensaje:", e.message);
        res.status(500).json({ error: "No se pudo enviar el mensaje" });
    }
});

startBot();

app.listen(3000, () => {
    console.log("🚀 Servidor de Baileys escuchando en http://localhost:3000");
});
