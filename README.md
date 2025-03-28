# 🛠️ KledBot - Instalación y Configuración

Este proyecto es una implementación completa de un chatbot inteligente para atención a clientes en WhatsApp utilizando OpenAI, ChromaDB, LangChain y Baileys.

---

## 📁 Estructura del Proyecto

```
kledbot/
├── bot.py                  # Servidor principal Flask
├── formulario.py           # Carga del formulario a ChromaDB
├── catalogo.py             # Carga del catálogo a ChromaDB
├── requirements.txt        # Dependencias del entorno
├── config.py               # Configuración general (tokens, paths)
├── kledbot/
│   ├── __init__.py
│   ├── chatbot.py          # Función principal para obtener respuesta de ChatGPT
│   ├── whatsapp.py         # Envío y recepción de mensajes usando Baileys
│   ├── catalogo.py         # Código para indexar productos
│   ├── formulario.py       # Código para indexar FAQs y respuestas del negocio
│   └── db/
│       └── chromadb/
│           ├── chroma_setup.py       # Configuración del cliente Chroma
│           └── chroma_queries.py     # Colecciones compartidas para búsqueda
├── baileys_auth/           # Directorio donde se guarda la sesión de Baileys
└── n8n/                    # Flujos automatizados
```

---

## 🧱 Requisitos Previos

- Ubuntu Server 22.04+
- Python 3.12+
- Node.js 18+
- pm2
- nginx

---

## ⚙️ Instalación de Dependencias

1. Crear entorno virtual:
```bash
python3 -m venv env
source env/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

---

## 💾 Base de Datos ChromaDB (Modo Integrado)

No es necesario ejecutar un servidor por separado. ChromaDB se usa en modo **in-process**, por lo que el código Python se encarga de gestionar la carga y persistencia automáticamente:

📁 Carpeta de persistencia: `./kledbot/db/chromadb_storage`

```python
chroma_client = chromadb.PersistentClient(path="./kledbot/db/chromadb_storage")
```

✅ El almacenamiento se realiza automáticamente cada vez que se insertan datos desde:
- `catalogo.py` → productos
- `formulario.py` → preguntas y respuestas frecuentes

---

## 📄 Cargar Catálogo y Formulario

1. Coloca `catalogoKled.xlsx` y `Formulario_Informacion.txt` en la raíz del proyecto.

2. Ejecuta los scripts para cargar los datos:
```bash
python catalogo.py
python formulario.py
```

---

## 🚀 Ejecutar el Bot con PM2 (persistente)

```bash
pm2 start bot.py --interpreter=python3 --name KledBot
pm2 save
pm2 startup
```

---

## 🎨 Personalización del Bash

Instala **Oh My Bash** con tema `agnoster`:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
sed -i 's/OSH_THEME=.*/OSH_THEME=agnoster/' ~/.bashrc
source ~/.bashrc
```

---

## 📬 Integración con WhatsApp

- Se usa **Baileys** como alternativa a la API oficial de Meta.
- El servidor Node.js (`server.js`) maneja el envío y recepción de mensajes desde WhatsApp.
- Los mensajes son enviados al webhook de Flask (bot.py), el cual procesa y responde usando ChatGPT + ChromaDB.

---

## 🌐 Comunicación entre Módulos

- `server.js` escucha mensajes nuevos desde WhatsApp y los reenvía por POST a `http://localhost:5000/webhook`
- `bot.py` recibe ese mensaje, consulta las bases ChromaDB y genera una respuesta usando OpenAI.
- `server.js` recibe la respuesta y la envía nuevamente al usuario en WhatsApp.

---

## 📌 Notas Finales

- No se requiere ejecutar `chromadb.run`, ya que el acceso es **in-process**.
- Toda la información cargada permanece disponible mientras no se borre el directorio `chromadb_storage/`.
- Verifica siempre que las colecciones existan (`catalogo`, `faq`) antes de ejecutar el bot.

---

✅ Listo para continuar con la siguiente fase.

