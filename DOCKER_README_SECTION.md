# Docker Compose Deployment

## 🐳 Quick Start with Docker

The Agent Factory can be deployed using Docker Compose for both development and production environments.

### Prerequisites
- Docker 24.0+ with Docker Compose V2
- 8GB+ RAM (16GB+ recommended for production)
- 10GB+ available disk space

### Development Deployment

```bash
# Quick start development environment
./scripts/dev-start.sh
```

This will:
- Create `.env` from template
- Build development containers with hot-reload
- Start all core services

### Production Deployment

```bash
# Configure production environment
cp .env.production.example .env.production
# Edit .env.production with your API keys and settings

# Deploy production environment
./scripts/prod-deploy.sh
```

## 🏗️ Architecture

### Core Services
- **agent-api**: FastAPI REST API & WebSocket gateway (port 8000)
- **redis**: Message bus for inter-agent communication (port 6379)
- **chromadb**: Vector database for knowledge storage (port 8001)

### Agent Services
- **agent-coordinator**: Task orchestration and workflow management
- **agent-planner**: Feature planning and PRP generation
- **agent-coder**: Code implementation and generation
- **agent-tester**: Automated testing and validation
- **agent-reviewer**: Code review and quality assurance
- **agent-devops**: Deployment and infrastructure operations

### Optional Services
- **agent-ui**: Streamlit dashboard (port 8501) - Profile: `ui`
- **prometheus**: Metrics collection (port 9090) - Profile: `monitoring`
- **grafana**: Metrics visualization (port 3000) - Profile: `monitoring`

## 🔧 Service Control

### Start Services
```bash
# Core services only
docker-compose up -d

# Include UI
docker-compose --profile ui up -d

# Include monitoring
docker-compose --profile monitoring up -d

# All services
docker-compose --profile ui --profile monitoring up -d
```

### Development with Hot-Reload
```bash
# Development mode with source code mounting
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Scale Individual Agents
```bash
# Scale coder agents for high workload
docker-compose up -d --scale agent-coder=3

# Scale tester agents for CI/CD
docker-compose up -d --scale agent-tester=2
```

### Management Commands
```bash
# View service status
docker-compose ps

# View logs
docker-compose logs -f agent-coordinator

# Check service health
docker-compose exec agent-api curl -f http://localhost:8000/health

# Stop services
docker-compose down

# Update and restart services
docker-compose pull && docker-compose up -d --force-recreate
```

## 📊 Monitoring

### Built-in Monitoring (with --profile monitoring)
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### Health Checks
All services include health checks:
```bash
# View health status
docker-compose ps
```

### Logs
```bash
# All services
docker-compose logs -f

# Specific service  
docker-compose logs -f agent-api

# Export logs to file
docker-compose logs --no-color > agent-factory.log
```

## 🔒 Security

### Production Security Features
- Non-root container execution
- Multi-stage builds with minimal runtime images
- Isolated Docker network (172.20.0.0/16)
- Health checks for all services
- Secure environment variable handling

### Environment Configuration
- Development: `.env` (auto-created from `.env.example`)
- Production: `.env.production` (must be manually configured)

## 📦 Data Persistence

### Persistent Volumes
- **redis_data**: Redis persistence and queues
- **chroma_data**: Vector database storage
- **prometheus_data**: Metrics storage (optional)
- **grafana_data**: Dashboard configuration (optional)

### Backup & Restore
```bash
# Backup ChromaDB data
docker run --rm -v agent-factory_chroma_data:/data -v $(pwd)/backup:/backup alpine tar czf /backup/chroma-backup.tar.gz /data

# Restore ChromaDB data  
docker run --rm -v agent-factory_chroma_data:/data -v $(pwd)/backup:/backup alpine tar xzf /backup/chroma-backup.tar.gz -C /
```

## 🚨 Troubleshooting

### Common Issues

#### Service won't start
```bash
# Check logs
docker-compose logs service-name

# Verify configuration
docker-compose config
```

#### Performance issues
```bash
# Check resource usage
docker stats

# Monitor message queues
docker-compose exec redis redis-cli monitor
```

#### Connection issues  
```bash
# Test Redis connection
docker-compose exec agent-api python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"

# Test ChromaDB connection
curl http://localhost:8001/api/v1/heartbeat
```

For comprehensive deployment documentation, see [DEPLOYMENT.md](DEPLOYMENT.md).
