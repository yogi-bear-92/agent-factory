#!/bin/bash

# Agent Factory Production Deployment Script
# This script deploys the production environment

set -e

echo "🚀 Deploying Agent Factory Production Environment..."

# Check if production env file exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production file not found!"
    echo "Please create .env.production with production configuration"
    exit 1
fi

# Validate required environment variables
echo "✅ Validating production configuration..."
source .env.production

required_vars=(
    "LLM_API_KEY"
    "API_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ] || [ "${!var}" = "your-openai-api-key-here" ] || [ "${!var}" = "production-secure-api-key-change-me" ]; then
        echo "❌ Required environment variable $var is not set or has default value"
        echo "Please update .env.production with proper values"
        exit 1
    fi
done

echo "✅ Configuration validated"

# Ensure directories exist with proper permissions
echo "📁 Creating production directories..."
sudo mkdir -p data/chroma
sudo mkdir -p logs
sudo chown -R 1000:1000 data logs
sudo chmod 755 data logs

# Pull latest images
echo "⬇️  Pulling production Docker images..."
docker-compose --env-file .env.production pull

# Build production containers
echo "🔨 Building production containers..."
docker-compose --env-file .env.production build --no-cache

# Stop existing services gracefully
echo "🛑 Stopping existing services..."
docker-compose --env-file .env.production down --timeout 30

# Start production services
echo "🎯 Starting production services..."
docker-compose --env-file .env.production up -d --remove-orphans

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health check
echo "🏥 Performing health checks..."
max_attempts=10
attempt=1

services=("redis" "chromadb" "agent-api")

for service in "${services[@]}"; do
    echo "Checking $service..."
    while [ $attempt -le $max_attempts ]; do
        if docker-compose --env-file .env.production ps $service | grep -q "healthy\|Up"; then
            echo "✅ $service is healthy"
            break
        else
            echo "⏳ Waiting for $service... (attempt $attempt/$max_attempts)"
            sleep 10
            attempt=$((attempt + 1))
        fi
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "❌ $service failed to become healthy"
        echo "Deployment may have issues. Check logs with: docker-compose --env-file .env.production logs $service"
    fi
    
    attempt=1
done

echo ""
echo "✅ Production deployment completed!"
echo ""
echo "🌐 Production services:"
echo "   - FastAPI API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo "   - ChromaDB: http://localhost:8001"
echo ""
echo "📊 Optional monitoring (add --profile monitoring):"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "🔧 Management commands:"
echo "   - View logs: docker-compose --env-file .env.production logs -f [service-name]"
echo "   - Check status: docker-compose --env-file .env.production ps"
echo "   - Stop services: docker-compose --env-file .env.production down"
