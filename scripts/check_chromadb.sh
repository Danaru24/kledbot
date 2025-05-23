#!/bin/bash

echo "🔎 Verificando estado del servidor ChromaDB..."

# Verificar si el contenedor está corriendo
if ! docker ps --format '{{.Names}}' | grep -q chromadb_server; then
  echo "❌ El contenedor 'chromadb_server' no está corriendo."
  echo "ℹ️ Ejecuta './run_chromadb.sh' para iniciarlo."
  exit 1
fi

# Verificar si responde en el puerto 8000 (aunque sea con un 404)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000)

if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "404" ]]; then
  echo "✅ El servidor ChromaDB está activo en http://localhost:8000 (HTTP $HTTP_CODE)"
  exit 0
else
  echo "⚠️ El contenedor está corriendo, pero no responde correctamente (HTTP $HTTP_CODE)"
  exit 2
fi
