# Agent Factory Docker Deployment Guide

This guide provides comprehensive instructions for deploying the Agent Factory multi-agent system using Docker Compose.

## 📋 Prerequisites

### System Requirements
- **Docker**: 24.0+ with Docker Compose V2
- **Memory**: Minimum 8GB RAM (16GB+ recommended for production)
- **Storage**: 10GB+ available disk space
- **CPU**: 4+ cores recommended
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2

### Required API Keys
- **OpenAI API Key** (or Azure OpenAI credentials)
- **Custom API Key** for internal authentication

## 🚀 Quick Start

### 1. Development Environment

```bash
# Clone repository
git clone <repository-url>
cd agent-factory

# Start development environment
./scripts/dev-start.sh
```

This will:
- Create `.env` from template
- Set up development containers with hot-reload
- Expose services on localhost ports

### 2. Production Environment

```bash
# Copy and configure production environment
cp .env.production.example .env.production

# Edit configuration (REQUIRED)
nano .env.production

# Deploy production environment
./scripts/prod-deploy.sh
```

## 🏗️ Architecture Overview

### Core Services

| Service | Purpose | Port | Dependencies |
|---------|---------|------|-------------|
| **agent-api** | FastAPI REST API & WebSocket gateway | 8000 | redis, chromadb |
| **redis** | Message bus for inter-agent communication | 6379 | none |
| **chromadb** | Vector database for knowledge storage | 8001 | none |

### Agent Services

| Agent | Purpose | Dependencies |
|-------|---------|-------------|
| **agent-coordinator** | Task orchestration and workflow management | redis, chromadb |
| **agent-planner** | Feature planning and PRP generation | redis, chromadb |
| **agent-coder** | Code implementation and generation | redis, chromadb |
| **agent-tester** | Automated testing and validation | redis, chromadb |
| **agent-reviewer** | Code review and quality assurance | redis, chromadb |
| **agent-devops** | Deployment and infrastructure operations | redis, chromadb |

### Optional Services

| Service | Purpose | Profile | Port |
|---------|---------|---------|------|
| **agent-ui** | Streamlit dashboard | ui | 8501 |
| **prometheus** | Metrics collection | monitoring | 9090 |
| **grafana** | Metrics visualization | monitoring | 3000 |

## ⚙️ Configuration

### Environment Files

- **`.env`**: Development configuration
- **`.env.production`**: Production configuration
- **`.env.example`**: Template with all available options

### Key Configuration Sections

#### LLM Configuration
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
LLM_API_KEY=your-openai-api-key-here
LLM_MAX_TOKENS=4000
LLM_TEMPERATURE=0.1
```

#### Azure OpenAI Alternative
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-05-01-preview
```

#### Agent System Tuning
```env
AGENT_MAX_CONCURRENT_AGENTS=5
AGENT_TASK_TIMEOUT=3600
AGENT_HEARTBEAT_INTERVAL=30
AGENT_MAX_RETRIES=3
AGENT_BACKOFF_FACTOR=2.0
```

## 🐳 Docker Compose Files

### Primary Files

1. **`docker-compose.yml`**: Base production configuration
2. **`docker-compose.dev.yml`**: Development overrides with hot-reload
3. **`.env.production`**: Production environment variables

### Service Profiles

Control which services to run using Docker Compose profiles:

```bash
# Core services only (default)
docker-compose up

# Include Streamlit UI
docker-compose --profile ui up

# Include monitoring stack
docker-compose --profile monitoring up

# All services
docker-compose --profile ui --profile monitoring up
```

## 📊 Deployment Commands

### Development Commands

```bash
# Start development environment
./scripts/dev-start.sh

# Start with specific services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up redis chromadb agent-api

# View logs
docker-compose logs -f agent-api

# Access development container
docker exec -it agent-factory-dev-tools bash

# Rebuild after code changes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build agent-api
```

### Production Commands

```bash
# Deploy production environment
./scripts/prod-deploy.sh

# Start specific profile
docker-compose --env-file .env.production --profile monitoring up -d

# Scale agents
docker-compose --env-file .env.production up -d --scale agent-coder=2

# Update services
docker-compose --env-file .env.production pull
docker-compose --env-file .env.production up -d --force-recreate

# Stop services
docker-compose --env-file .env.production down
```

### Monitoring Commands

```bash
# View all service status
docker-compose ps

# Check service health
docker-compose exec agent-api curl -f http://localhost:8000/health

# View resource usage
docker stats

# Access logs
docker-compose logs -f --tail=100 agent-coordinator
```

## 🔧 Service Management

### Health Checks

All services include health checks with configurable parameters:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Volume Management

```bash
# List volumes
docker volume ls

# Backup ChromaDB data
docker run --rm -v agent-factory_chroma_data:/data -v $(pwd)/backup:/backup alpine tar czf /backup/chroma-backup.tar.gz /data

# Restore ChromaDB data
docker run --rm -v agent-factory_chroma_data:/data -v $(pwd)/backup:/backup alpine tar xzf /backup/chroma-backup.tar.gz -C /
```

### Network Configuration

Services communicate via the `agent-network` bridge network with subnet `172.20.0.0/16`.

## 📈 Monitoring & Observability

### Metrics Collection

Enable Prometheus metrics collection:

```env
MONITORING_ENABLE_METRICS=true
MONITORING_METRICS_PORT=9090
```

### Log Aggregation

Logs are structured using Python's `structlog`:

```bash
# View aggregated logs
docker-compose logs -f | grep ERROR

# Export logs to file
docker-compose logs --no-color > agent-factory.log
```

### Performance Monitoring

Access Grafana dashboard at `http://localhost:3000`:
- Username: `admin`
- Password: `admin`

Pre-configured dashboards include:
- Agent performance metrics
- Redis message queue statistics  
- ChromaDB vector operations
- API response times and error rates

## 🚨 Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check service logs
docker-compose logs service-name

# Verify configuration
docker-compose config

# Check disk space
df -h
```

#### Connection Issues
```bash
# Test Redis connectivity
docker-compose exec agent-api python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"

# Test ChromaDB connectivity
curl http://localhost:8001/api/v1/heartbeat
```

#### Performance Issues
```bash
# Check resource usage
docker stats

# Monitor agent queue
docker-compose exec redis redis-cli monitor

# Check ChromaDB collections
curl http://localhost:8001/api/v1/collections
```

### Debug Mode

Enable debug mode in development:

```env
DEBUG=true
MONITORING_LOG_LEVEL=DEBUG
```

This provides:
- Verbose logging
- Extended timeouts
- Development error pages
- Auto-reload on code changes

## 🔒 Security Considerations

### Production Security

1. **API Keys**: Never commit real API keys to version control
2. **Network Access**: Use Docker secrets for sensitive data
3. **Container Security**: Run containers as non-root user
4. **Firewall**: Restrict external access to necessary ports only

### Environment Variables Security

```bash
# Use Docker secrets in production
echo "your-api-key" | docker secret create openai_api_key -

# Reference in compose file
secrets:
  - openai_api_key
```

### SSL/TLS Configuration

For production deployments, use a reverse proxy (nginx/traefik) with SSL:

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "443:443"
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./ssl:/etc/ssl
```

## 📦 Scaling & Production Deployment

### Horizontal Scaling

Scale individual agents based on workload:

```bash
# Scale coder agents for high development workload
docker-compose --env-file .env.production up -d --scale agent-coder=3

# Scale tester agents for CI/CD pipeline
docker-compose --env-file .env.production up -d --scale agent-tester=2
```

### Resource Limits

Configure resource limits in production:

```yaml
services:
  agent-coder:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'  
          memory: 2G
```

### Multi-Node Deployment

For multi-node deployment, consider:
- Docker Swarm mode
- Kubernetes deployment
- External Redis cluster
- Distributed ChromaDB setup

## 🔄 Updates & Maintenance

### Rolling Updates

```bash
# Update single service
docker-compose --env-file .env.production pull agent-api
docker-compose --env-file .env.production up -d --no-deps agent-api

# Update all services with zero-downtime
./scripts/rolling-update.sh
```

### Backup Strategy

```bash
# Full backup script
./scripts/backup.sh

# Automated backup (crontab)
0 2 * * * cd /opt/agent-factory && ./scripts/backup.sh
```

## 📞 Support & Maintenance

### Log Locations
- Application logs: `./logs/`
- Container logs: `docker-compose logs`
- System logs: `/var/lib/docker/containers/`

### Useful Commands

```bash
# Complete system reset (DANGER: Destroys all data)
docker-compose down -v
docker system prune -a --volumes

# Partial reset (keeps volumes)
docker-compose down
docker-compose up -d --force-recreate
```

This deployment guide provides a comprehensive foundation for running the Agent Factory system in both development and production environments with proper monitoring, security, and maintenance considerations.
