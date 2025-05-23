#!/bin/bash

STORAGE_PATH="/root/kledbot/kledbot/db/chromadb/chromadb_storage"
CONTAINER_NAME="chromadb_server"

echo "📦 Verificando contenedor previo..."

# Si el contenedor ya existe, lo eliminamos
if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
  echo "🧹 Eliminando contenedor anterior..."
  docker stop $CONTAINER_NAME >/dev/null 2>&1
  docker rm $CONTAINER_NAME >/dev/null 2>&1
fi

echo "🚀 Iniciando nuevo servidor ChromaDB v0.6.3..."
docker run -d \
  --name $CONTAINER_NAME \
  -p 8000:8000 \
  -v "$STORAGE_PATH":/chroma-data \
  -e CHROMA_PERSIST_DIRECTORY=/chroma-data \
  ghcr.io/chroma-core/chroma:0.6.3


echo "✅ ChromaDB está disponible en http://localhost:8000"
