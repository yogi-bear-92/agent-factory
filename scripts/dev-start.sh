#!/bin/bash

# Agent Factory Development Startup Script
# This script starts the development environment with hot-reload

set -e

echo "🚀 Starting Agent Factory Development Environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys and configuration"
fi

# Ensure directories exist
echo "📁 Creating necessary directories..."
mkdir -p data/chroma
mkdir -p logs
chmod 755 data logs

# Pull latest images
echo "⬇️  Pulling latest Docker images..."
docker-compose pull redis chromadb

# Build development containers
echo "🔨 Building development containers..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build --parallel

# Start development services
echo "🎯 Starting development services..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --remove-orphans

echo "✅ Development environment started!"
echo ""
echo "🌐 Available services:"
echo "   - FastAPI: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Redis: localhost:6379"
echo "   - ChromaDB: http://localhost:8001"
echo ""
echo "📊 Optional services (use --profile flag):"
echo "   - Streamlit UI: docker-compose --profile ui up"
echo "   - Monitoring: docker-compose --profile monitoring up"
echo ""
echo "🛠️  Development tools:"
echo "   - Access dev container: docker exec -it agent-factory-dev-tools bash"
echo "   - View logs: docker-compose logs -f [service-name]"
