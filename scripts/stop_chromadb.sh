#!/bin/bash

echo "🛑 Deteniendo y eliminando el contenedor de ChromaDB..."

docker stop chromadb_server && docker rm chromadb_server

echo "✅ Contenedor detenido y eliminado."
