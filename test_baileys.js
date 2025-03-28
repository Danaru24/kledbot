const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } = require("@whiskeysockets/baileys");
const { Boom } = require("@hapi/boom");
const fs = require("fs");
global.crypto = require("crypto");  // 👈 NECESARIO para que Baileys funcione correctamente

async function iniciar() {
  const { state, saveCreds } = await useMultiFileAuthState("baileys_auth");

  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    auth: state,
    printQRInTerminal: true
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", (update) => {
    const { connection, lastDisconnect } = update;
    if (connection === "close") {
      const shouldReconnect = (lastDisconnect?.error instanceof Boom)
        ? lastDisconnect.error.output?.statusCode !== DisconnectReason.loggedOut
        : true;

      console.log("❌ Conexión cerrada. Reintentando:", shouldReconnect);
      if (shouldReconnect) {
        iniciar();  // reintenta
      }
    } else if (connection === "open") {
      console.log("✅ Conectado exitosamente a WhatsApp");
    }
  });

  sock.ev.on("messages.upsert", ({ messages }) => {
    console.log("📩 Mensaje recibido:", messages[0]?.message?.conversation);
  });
}

iniciar();
