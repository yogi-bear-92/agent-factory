# Agent Factory - Configuration Guide

Complete configuration reference for setting up and tuning the Agent Factory autonomous development system.

## Table of Contents

- [Quick Setup](#quick-setup)
- [Environment Variables](#environment-variables)
- [Agent Configuration](#agent-configuration)
- [LLM Provider Configuration](#llm-provider-configuration)
- [Database Configuration](#database-configuration)
- [Docker Configuration](#docker-configuration)
- [Security Settings](#security-settings)
- [Performance Tuning](#performance-tuning)
- [Monitoring Configuration](#monitoring-configuration)
- [Production Deployment](#production-deployment)

## Quick Setup

### Minimal Setup for Development

```bash
# 1. Clone and setup environment
git clone <repository>
cd agent-factory
cp .env.example .env

# 2. Install dependencies
uv sync

# 3. Start infrastructure services
docker-compose up -d redis chroma postgres

# 4. Configure LLM provider (choose one)
export OPENAI_API_KEY="your-openai-key"
# OR
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"

# 5. Start the system
uv run uvicorn src.api.rest.app:app --reload
```

### Full Production Setup

```bash
# 1. Environment configuration
cp .env.example .env.production
# Edit .env.production with production values

# 2. Infrastructure deployment
docker-compose -f docker-compose.prod.yml up -d

# 3. Initialize knowledge base
uv run python scripts/init_knowledge_base.py

# 4. Start agent services
docker-compose -f docker-compose.agents.yml up -d

# 5. Verify deployment
curl http://localhost:8080/health
```

## Environment Variables

### Core System Variables

```bash
# Application Settings
ENVIRONMENT=development|staging|production
DEBUG=true|false
API_VERSION=v1
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
API_WORKERS=4
API_RELOAD=true|false

# Security
SECRET_KEY=your-secret-key-here
API_KEY_SALT=your-api-key-salt
JWT_SECRET=your-jwt-secret
SESSION_TIMEOUT=3600

# Feature Flags
ENABLE_WEBSOCKETS=true
ENABLE_UI=true
ENABLE_MONITORING=true
ENABLE_RATE_LIMITING=true
```

### Database Configuration

```bash
# PostgreSQL (Metadata)
DATABASE_URL=postgresql://user:password@host:5432/agent_factory
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agent_factory
DB_USER=agent_factory
DB_PASSWORD=your-secure-password
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30

# Redis (Message Bus & Cache)
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your-redis-password
REDIS_SSL=true|false
REDIS_POOL_SIZE=10

# Chroma (Vector Database)
CHROMA_URL=http://localhost:8000
CHROMA_HOST=localhost  
CHROMA_PORT=8000
CHROMA_COLLECTION=agent_knowledge
CHROMA_PERSIST_DIRECTORY=./data/chroma
```

### LLM Provider Configuration

#### OpenAI Configuration
```bash
# OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=4096
OPENAI_TEMPERATURE=0.1
OPENAI_REQUEST_TIMEOUT=60
OPENAI_MAX_RETRIES=3

# Optional: Organization and Project
OPENAI_ORG_ID=org-your-org-id
OPENAI_PROJECT_ID=proj_your-project-id
```

#### Azure OpenAI Configuration
```bash
# Azure OpenAI
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4-turbo
AZURE_OPENAI_API_VERSION=2024-05-01-preview
AZURE_OPENAI_MAX_TOKENS=4096
AZURE_OPENAI_TEMPERATURE=0.1
```

#### Local/Self-Hosted LLM Configuration
```bash
# Local LLM (Ollama, etc.)
LLM_PROVIDER=local
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=llama3.1:8b-instruct-q4_0
LOCAL_LLM_CONTEXT_SIZE=8192
LOCAL_LLM_TEMPERATURE=0.1
```

### Agent Configuration

```bash
# Global Agent Settings
AGENT_DEFAULT_TIMEOUT=300
AGENT_MAX_RETRIES=3
AGENT_HEARTBEAT_INTERVAL=30
AGENT_MEMORY_LIMIT=4Gi
AGENT_CPU_LIMIT=2.0

# Coordinator Settings
COORDINATOR_MAX_CONCURRENT_FEATURES=10
COORDINATOR_TASK_TIMEOUT=1800
COORDINATOR_DEPENDENCY_TIMEOUT=300

# Planner Settings  
PLANNER_MAX_TASK_DEPTH=5
PLANNER_CONTEXT_SIZE=4000
PLANNER_PLANNING_TIMEOUT=600

# Coder Settings
CODER_MAX_CONCURRENT_TASKS=3
CODER_CODE_GENERATION_TIMEOUT=900
CODER_PREFERRED_LANGUAGES=python,javascript,typescript
CODER_MAX_FILE_SIZE=100KB

# Tester Settings
TESTER_COVERAGE_THRESHOLD=0.95
TESTER_MAX_TEST_DURATION=1800
TESTER_PARALLEL_TESTS=4

# Reviewer Settings
REVIEWER_MAX_FILES_PER_REVIEW=20
REVIEWER_SECURITY_SCAN=true
REVIEWER_PERFORMANCE_CHECK=true

# DevOps Settings
DEVOPS_DEFAULT_REGISTRY=docker.io/yourorg
DEVOPS_DEPLOYMENT_TIMEOUT=1800
DEVOPS_HEALTH_CHECK_TIMEOUT=300
```

## Agent Configuration

### Per-Agent Configuration Files

#### Task Coordinator (`config/agents/coordinator.yml`)
```yaml
coordinator:
  name: "Task Coordinator"
  version: "1.0.0"
  
  capabilities:
    - task_orchestration
    - dependency_management
    - resource_allocation
    - progress_tracking
  
  settings:
    max_concurrent_features: 10
    task_assignment_timeout: 30
    dependency_resolution_depth: 5
    progress_reporting_interval: 60
    
  resource_limits:
    memory: "1Gi"
    cpu: "0.5"
    
  scaling:
    min_instances: 1
    max_instances: 3
    target_cpu_utilization: 70
```

#### Feature Planner (`config/agents/planner.yml`)
```yaml
planner:
  name: "Feature Planner"
  version: "1.0.0"
  
  capabilities:
    - requirements_analysis
    - task_decomposition
    - dependency_identification
    - prp_generation
    
  settings:
    max_task_breakdown_depth: 5
    context_retrieval_limit: 10
    planning_timeout: 600
    prp_template: "comprehensive"
    
  llm_settings:
    model: "gpt-4-turbo-preview"
    temperature: 0.1
    max_tokens: 4096
    
  resource_limits:
    memory: "2Gi"
    cpu: "1.0"
```

#### Implementation Coder (`config/agents/coder.yml`)
```yaml
coder:
  name: "Implementation Coder"
  version: "1.0.0"
  
  capabilities:
    - python_development
    - javascript_development
    - api_implementation
    - database_integration
    - test_writing
    
  settings:
    max_concurrent_tasks: 3
    code_generation_timeout: 900
    max_file_size: "100KB"
    preferred_frameworks:
      python: ["FastAPI", "SQLAlchemy", "Pydantic"]
      javascript: ["React", "Next.js", "Express"]
    coding_standards:
      python: "PEP8"
      javascript: "ESLint + Prettier"
      
  quality_gates:
    syntax_check: true
    style_check: true
    security_scan: true
    
  resource_limits:
    memory: "4Gi"
    cpu: "2.0"
    
  scaling:
    min_instances: 1
    max_instances: 5
    scale_up_threshold: 80
```

### Agent-Specific Environment Variables

```bash
# Per-agent overrides
COORDINATOR_MEMORY_LIMIT=1Gi
COORDINATOR_CPU_LIMIT=0.5
COORDINATOR_INSTANCES=1

PLANNER_MEMORY_LIMIT=2Gi
PLANNER_CPU_LIMIT=1.0
PLANNER_INSTANCES=1

CODER_MEMORY_LIMIT=4Gi
CODER_CPU_LIMIT=2.0
CODER_INSTANCES=3

TESTER_MEMORY_LIMIT=2Gi
TESTER_CPU_LIMIT=1.5
TESTER_INSTANCES=2

REVIEWER_MEMORY_LIMIT=1Gi
REVIEWER_CPU_LIMIT=1.0
REVIEWER_INSTANCES=1

DEVOPS_MEMORY_LIMIT=1Gi
DEVOPS_CPU_LIMIT=0.5
DEVOPS_INSTANCES=1
```

## LLM Provider Configuration

### OpenAI Configuration

```python
# config/llm/openai.py
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
    "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "4096")),
    "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
    "timeout": int(os.getenv("OPENAI_REQUEST_TIMEOUT", "60")),
    "max_retries": int(os.getenv("OPENAI_MAX_RETRIES", "3")),
    "organization": os.getenv("OPENAI_ORG_ID"),
    "project": os.getenv("OPENAI_PROJECT_ID"),
    
    # Rate limiting
    "requests_per_minute": 500,
    "tokens_per_minute": 160000,
    
    # Model-specific settings
    "models": {
        "gpt-4-turbo-preview": {
            "context_window": 128000,
            "max_output_tokens": 4096,
            "cost_per_1k_input": 0.01,
            "cost_per_1k_output": 0.03
        },
        "gpt-3.5-turbo": {
            "context_window": 16385,
            "max_output_tokens": 4096,
            "cost_per_1k_input": 0.0015,
            "cost_per_1k_output": 0.002
        }
    }
}
```

### Azure OpenAI Configuration

```python
# config/llm/azure.py
AZURE_OPENAI_CONFIG = {
    "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview"),
    "max_tokens": int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "4096")),
    "temperature": float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0.1")),
    
    # Azure-specific settings
    "content_filter": {
        "hate": {"blocked": True, "severity_threshold": "medium"},
        "self_harm": {"blocked": True, "severity_threshold": "medium"},
        "sexual": {"blocked": True, "severity_threshold": "medium"},
        "violence": {"blocked": True, "severity_threshold": "medium"}
    },
    
    # Retry configuration
    "retry_config": {
        "max_retries": 3,
        "backoff_factor": 2.0,
        "status_forcelist": [429, 500, 502, 503, 504]
    }
}
```

## Database Configuration

### PostgreSQL Configuration

```bash
# postgresql.conf adjustments for production
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200

# Agent Factory specific settings
work_mem = 4MB
max_parallel_workers_per_gather = 2
max_parallel_workers = 8
max_parallel_maintenance_workers = 2
```

### Redis Configuration

```bash
# redis.conf adjustments
maxmemory 512mb
maxmemory-policy allkeys-lru
timeout 300
tcp-keepalive 60

# Pub/sub specific settings
client-output-buffer-limit pubsub 32mb 8mb 60

# Persistence settings
save 900 1
save 300 10
save 60 10000
```

### Chroma Configuration

```python
# config/chroma.py
CHROMA_CONFIG = {
    "host": os.getenv("CHROMA_HOST", "localhost"),
    "port": int(os.getenv("CHROMA_PORT", "8000")),
    "collection_name": os.getenv("CHROMA_COLLECTION", "agent_knowledge"),
    "persist_directory": os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma"),
    
    # Embedding settings
    "embedding_function": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dimension": 384,
    
    # Performance settings
    "batch_size": 100,
    "max_batch_size": 1000,
    "query_limit": 10,
    
    # Collection settings
    "collections": {
        "agent_knowledge": {
            "metadata": {"hnsw:space": "cosine"},
            "embedding_function": "sentence-transformers/all-MiniLM-L6-v2"
        },
        "code_patterns": {
            "metadata": {"hnsw:space": "cosine", "hnsw:M": 16},
            "embedding_function": "sentence-transformers/all-MiniLM-L6-v2"
        }
    }
}
```

## Docker Configuration

### Development Docker Compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # Infrastructure
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=agent_factory
      - POSTGRES_USER=agent_factory
      - POSTGRES_PASSWORD=${DB_PASSWORD:-password}

  # Application Services
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ENVIRONMENT=development
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_URL=http://chroma:8000
      - DATABASE_URL=postgresql://agent_factory:${DB_PASSWORD:-password}@postgres:5432/agent_factory
    volumes:
      - ./src:/app/src
      - ./config:/app/config
    depends_on:
      - redis
      - chroma
      - postgres
    command: uvicorn src.api.rest.app:app --host ******* --port 8080 --reload

volumes:
  redis_data:
  chroma_data:
  postgres_data:
```

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Infrastructure with production settings
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: >
      redis-server 
      --appendonly yes 
      --maxmemory 512mb 
      --maxmemory-policy allkeys-lru
      --requirepass ${REDIS_PASSWORD}

  chroma:
    image: chromadb/chroma:latest
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
      - CHROMA_AUTH_PROVIDER=basic
      - CHROMA_AUTH_CREDENTIALS=${CHROMA_AUTH_CREDENTIALS}

  postgres:
    image: postgres:15
    restart: unless-stopped
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./config/postgres/postgresql.conf:/etc/postgresql/postgresql.conf
    environment:
      - POSTGRES_DB=agent_factory
      - POSTGRES_USER=agent_factory
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    command: postgres -c 'config_file=/etc/postgresql/postgresql.conf'

  # Load balancer
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./config/ssl:/etc/ssl/certs
    depends_on:
      - api

  # Application services with scaling
  api:
    build: 
      context: .
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - ENVIRONMENT=production
      - API_WORKERS=4
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - CHROMA_URL=http://chroma:8000
      - DATABASE_URL=postgresql://agent_factory:${DB_PASSWORD}@postgres:5432/agent_factory
    depends_on:
      - redis
      - chroma
      - postgres
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'

volumes:
  redis_data:
  chroma_data:
  postgres_data:
```

### Agent Services Compose

```yaml
# docker-compose.agents.yml
version: '3.8'

services:
  coordinator:
    build: .
    restart: unless-stopped
    environment:
      - AGENT_TYPE=coordinator
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - CHROMA_URL=http://chroma:8000
    command: python -m src.agents.coordinator
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

  planner:
    build: .
    restart: unless-stopped
    environment:
      - AGENT_TYPE=planner
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - CHROMA_URL=http://chroma:8000
    command: python -m src.agents.planner
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 2G
          cpus: '1.0'

  coder:
    build: .
    restart: unless-stopped
    environment:
      - AGENT_TYPE=coder
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - CHROMA_URL=http://chroma:8000
    command: python -m src.agents.coder
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 4G
          cpus: '2.0'

  tester:
    build: .
    restart: unless-stopped
    environment:
      - AGENT_TYPE=tester
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - CHROMA_URL=http://chroma:8000
    command: python -m src.agents.tester
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 2G
          cpus: '1.5'

  reviewer:
    build: .
    restart: unless-stopped
    environment:
      - AGENT_TYPE=reviewer
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - CHROMA_URL=http://chroma:8000
    command: python -m src.agents.reviewer
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 1G
          cpus: '1.0'

  devops:
    build: .
    restart: unless-stopped
    environment:
      - AGENT_TYPE=devops
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - CHROMA_URL=http://chroma:8000
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: python -m src.agents.devops
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

networks:
  default:
    external:
      name: agent_factory_network
```

## Security Settings

### API Security Configuration

```python
# config/security.py
SECURITY_CONFIG = {
    # Authentication
    "jwt": {
        "secret_key": os.getenv("JWT_SECRET"),
        "algorithm": "HS256",
        "access_token_expire_minutes": 30,
        "refresh_token_expire_days": 7
    },
    
    # API Keys
    "api_keys": {
        "salt": os.getenv("API_KEY_SALT"),
        "hash_algorithm": "sha256",
        "key_length": 32,
        "rate_limit": {
            "requests_per_minute": 100,
            "burst_size": 20
        }
    },
    
    # CORS
    "cors": {
        "allow_origins": [
            "http://localhost:3000",  # React dev server
            "http://localhost:8080",  # API server
            os.getenv("FRONTEND_URL", "")
        ],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["*"]
    },
    
    # Rate limiting
    "rate_limiting": {
        "enabled": True,
        "storage": "redis",
        "default_limits": "100/minute",
        "per_endpoint": {
            "/features": "10/hour",
            "/agents/config": "5/minute"
        }
    }
}
```

### SSL/TLS Configuration

```nginx
# config/nginx/nginx.conf
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/certs/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    location / {
        proxy_pass http://api:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://api:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## Performance Tuning

### Application Performance

```python
# config/performance.py
PERFORMANCE_CONFIG = {
    # Async settings
    "async": {
        "max_workers": 10,
        "task_timeout": 300,
        "gather_timeout": 600
    },
    
    # Connection pooling
    "database": {
        "pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
        "pool_recycle": 3600
    },
    
    "redis": {
        "connection_pool_size": 20,
        "retry_on_timeout": True,
        "health_check_interval": 30
    },
    
    # Caching
    "cache": {
        "default_ttl": 3600,
        "knowledge_base_ttl": 7200,
        "agent_status_ttl": 60,
        "feature_status_ttl": 300
    },
    
    # Resource limits
    "memory": {
        "max_knowledge_entries": 10000,
        "max_conversation_history": 100,
        "context_window_limit": 8192
    }
}
```

### Infrastructure Tuning

```yaml
# Kubernetes resource configuration
resources:
  coordinator:
    requests:
      memory: "512Mi"
      cpu: "0.25"
    limits:
      memory: "1Gi"
      cpu: "0.5"
      
  planner:
    requests:
      memory: "1Gi"
      cpu: "0.5"
    limits:
      memory: "2Gi"
      cpu: "1.0"
      
  coder:
    requests:
      memory: "2Gi"
      cpu: "1.0"
    limits:
      memory: "4Gi"
      cpu: "2.0"

# Horizontal Pod Autoscaling
hpa:
  coder:
    min_replicas: 1
    max_replicas: 10
    target_cpu_utilization: 70
    target_memory_utilization: 80
```

## Monitoring Configuration

### Prometheus Metrics

```python
# config/monitoring.py
MONITORING_CONFIG = {
    "prometheus": {
        "enabled": True,
        "port": 9090,
        "metrics": {
            # Agent metrics
            "agent_task_duration_seconds": "histogram",
            "agent_task_total": "counter",
            "agent_errors_total": "counter",
            "agent_status": "gauge",
            
            # System metrics
            "http_requests_total": "counter",
            "http_request_duration_seconds": "histogram",
            "active_connections": "gauge",
            "knowledge_base_queries_total": "counter"
        }
    },
    
    "logging": {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "format": "json",
        "handlers": {
            "console": {"enabled": True},
            "file": {
                "enabled": True,
                "path": "/var/log/agent-factory/app.log",
                "rotation": "10MB"
            },
            "elasticsearch": {
                "enabled": False,
                "hosts": ["elasticsearch:9200"],
                "index": "agent-factory-logs"
            }
        }
    }
}
```

### Health Check Configuration

```python
# config/health.py
HEALTH_CONFIG = {
    "checks": {
        "database": {
            "timeout": 5,
            "query": "SELECT 1"
        },
        "redis": {
            "timeout": 5,
            "command": "ping"
        },
        "chroma": {
            "timeout": 10,
            "endpoint": "/api/v1/version"
        },
        "agents": {
            "timeout": 15,
            "check_interval": 30,
            "required_agents": [
                "coordinator",
                "planner", 
                "coder"
            ]
        }
    },
    
    "intervals": {
        "liveness": 30,
        "readiness": 10,
        "startup": 60
    }
}
```

## Production Deployment

### Environment-Specific Configurations

```bash
# .env.production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-production-secret-key
JWT_SECRET=your-production-jwt-secret
API_KEY_SALT=your-production-salt

# Database (use managed services in production)
DATABASE_URL=postgresql://user:pass@prod-postgres:5432/agent_factory
REDIS_URL=redis://prod-redis:6379/0
CHROMA_URL=http://prod-chroma:8000

# LLM Provider
OPENAI_API_KEY=your-production-api-key
OPENAI_ORG_ID=your-org-id

# Performance
API_WORKERS=8
REDIS_POOL_SIZE=20
DB_POOL_SIZE=20

# Monitoring
ENABLE_MONITORING=true
PROMETHEUS_PORT=9090

# Scaling
CODER_INSTANCES=5
TESTER_INSTANCES=3
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-factory-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-factory-api
  template:
    metadata:
      labels:
        app: agent-factory-api
    spec:
      containers:
      - name: api
        image: agent-factory:latest
        ports:
        - containerPort: 8080
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: agent-factory-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: agent-factory-secrets
              key: redis-url
        resources:
          requests:
            memory: "1Gi"
            cpu: "0.5"
          limits:
            memory: "2Gi"
            cpu: "1.0"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Configuration Validation

### Validation Script

```python
# scripts/validate_config.py
import os
import sys
from urllib.parse import urlparse

def validate_environment():
    """Validate all required environment variables."""
    required_vars = [
        "ENVIRONMENT",
        "SECRET_KEY",
        "DATABASE_URL",
        "REDIS_URL",
        "CHROMA_URL"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def validate_connections():
    """Test connections to external services."""
    # Add connection tests here
    pass

if __name__ == "__main__":
    if not validate_environment():
        sys.exit(1)
    print("✅ Configuration validation passed")
```

For troubleshooting configuration issues, see the [Troubleshooting Guide](TROUBLESHOOTING.md).

For deployment architecture details, see the [Architecture Documentation](ARCHITECTURE.md).
