# Agent Factory - Troubleshooting Guide

Complete troubleshooting reference for resolving common issues with the Agent Factory autonomous development system.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Installation & Setup Issues](#installation--setup-issues)
- [Agent Communication Problems](#agent-communication-problems)
- [Knowledge Base Issues](#knowledge-base-issues)
- [PRP Execution Failures](#prp-execution-failures)
- [Performance Issues](#performance-issues)
- [Log Analysis](#log-analysis)
- [Network & Connectivity](#network--connectivity)
- [Database Issues](#database-issues)
- [Security & Authentication](#security--authentication)
- [FAQ](#faq)

## Quick Diagnostics

### System Health Check

Run this comprehensive health check first:

```bash
# Check system status
curl http://localhost:8080/health

# Check all services
docker-compose ps

# Check agent status
curl http://localhost:8080/agents

# Check logs for errors
docker-compose logs --tail=50
```

### Expected Healthy Response
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development",
  "components": {
    "database": "healthy",
    "redis": "healthy", 
    "vector_store": "healthy",
    "agents": {
      "coordinator": "running",
      "planner": "running",
      "coder": "running",
      "tester": "running",
      "reviewer": "running",
      "devops": "running"
    }
  }
}
```

### Common Red Flags

🚨 **Immediate attention needed if you see:**
- `"status": "unhealthy"`
- Any agent with `"status": "offline"`
- `"database": "unhealthy"`
- `"redis": "unhealthy"`
- HTTP 500+ errors on `/health`

## Installation & Setup Issues

### Python Environment Issues

#### Problem: `uv sync` fails with dependency conflicts
```bash
ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**
1. **Check Python version:**
   ```bash
   python --version  # Should be 3.12+
   uv python install 3.12
   ```

2. **Clear cache and retry:**
   ```bash
   uv cache clean
   rm uv.lock
   uv sync
   ```

3. **Use specific Python version:**
   ```bash
   uv sync --python=3.12
   ```

#### Problem: Import errors after installation
```python
ModuleNotFoundError: No module named 'agent_factory'
```

**Solutions:**
1. **Ensure virtual environment is activated:**
   ```bash
   source .venv/bin/activate  # or 
   uv run python -c "import sys; print(sys.prefix)"
   ```

2. **Install in development mode:**
   ```bash
   uv pip install -e .
   ```

### Docker Issues

#### Problem: Docker services won't start
```bash
ERROR: Couldn't connect to Docker daemon
```

**Solutions:**
1. **Check Docker daemon:**
   ```bash
   docker info
   systemctl start docker  # Linux
   open -a Docker  # macOS
   ```

2. **Check port conflicts:**
   ```bash
   lsof -i :8080  # API port
   lsof -i :6379  # Redis port
   lsof -i :8000  # Chroma port
   ```

3. **Reset Docker state:**
   ```bash
   docker-compose down -v
   docker system prune -f
   docker-compose up -d
   ```

#### Problem: Container exits immediately
```bash
agent-factory-api-1 exited with code 1
```

**Diagnosis:**
```bash
# Check container logs
docker-compose logs api

# Check specific container
docker logs agent-factory-api-1

# Run container interactively
docker-compose run api bash
```

**Common fixes:**
- Environment variables not set properly
- Missing database migrations
- Port already in use
- Insufficient memory allocation

### Environment Configuration

#### Problem: Missing environment variables
```bash
KeyError: 'OPENAI_API_KEY'
```

**Solutions:**
1. **Check .env file exists:**
   ```bash
   ls -la .env*
   cp .env.example .env
   ```

2. **Validate required variables:**
   ```bash
   python scripts/validate_config.py
   ```

3. **Common missing variables:**
   ```bash
   # Add to .env
   OPENAI_API_KEY=your-key-here
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:pass@localhost:5432/agent_factory
   REDIS_URL=redis://localhost:6379/0
   CHROMA_URL=http://localhost:8000
   ```

## Agent Communication Problems

### Redis Connection Issues

#### Problem: Agents can't communicate
```bash
redis.exceptions.ConnectionError: Connection refused
```

**Diagnostics:**
```bash
# Test Redis connection
redis-cli ping

# Check Redis logs
docker-compose logs redis

# Test from Python
python -c "import redis; r=redis.Redis(); print(r.ping())"
```

**Solutions:**
1. **Restart Redis:**
   ```bash
   docker-compose restart redis
   ```

2. **Check Redis configuration:**
   ```bash
   # redis.conf
   bind 0.0.0.0
   protected-mode no
   port 6379
   ```

3. **Network connectivity:**
   ```bash
   # Test from agent container
   docker-compose exec coordinator ping redis
   ```

### Message Bus Issues

#### Problem: Messages not reaching agents
```bash
WARNING: No handler for message type: TASK_ASSIGNMENT
```

**Diagnostics:**
```bash
# Monitor Redis pub/sub
redis-cli monitor

# Check agent subscriptions
redis-cli pubsub channels

# Check message queue lengths
redis-cli llen agent.coordinator
```

**Solutions:**
1. **Restart agent services:**
   ```bash
   docker-compose restart coordinator planner coder
   ```

2. **Check message format:**
   ```python
   # Ensure proper message structure
   message = AgentMessage(
       sender_id="coordinator",
       recipient_id="coder", 
       message_type=MessageType.TASK_ASSIGNMENT,
       payload={"task": task.to_dict()}
   )
   ```

### Agent Status Issues

#### Problem: Agents showing as offline
```json
{
  "coordinator": "offline",
  "planner": "offline"
}
```

**Diagnostics:**
```bash
# Check agent processes
docker-compose ps

# Check agent logs
docker-compose logs coordinator
docker-compose logs planner

# Check resource usage
docker stats
```

**Solutions:**
1. **Resource exhaustion:**
   ```bash
   # Increase memory limits
   # docker-compose.yml
   services:
     coordinator:
       deploy:
         resources:
           limits:
             memory: 2G
   ```

2. **Restart agents:**
   ```bash
   docker-compose restart coordinator planner coder tester reviewer devops
   ```

3. **Check heartbeat configuration:**
   ```python
   # config/agents.py
   AGENT_HEARTBEAT_INTERVAL = 30  # seconds
   AGENT_HEARTBEAT_TIMEOUT = 90   # seconds
   ```

## Knowledge Base Issues

### Chroma Database Problems

#### Problem: Vector database not responding
```bash
requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=8000)
```

**Diagnostics:**
```bash
# Test Chroma API
curl http://localhost:8000/api/v1/version

# Check Chroma logs
docker-compose logs chroma

# Check disk space
df -h
```

**Solutions:**
1. **Restart Chroma:**
   ```bash
   docker-compose restart chroma
   ```

2. **Clear Chroma data (destructive):**
   ```bash
   docker-compose down
   docker volume rm agent-factory_chroma_data
   docker-compose up -d chroma
   ```

3. **Check persistence directory:**
   ```bash
   # Ensure directory exists and is writable
   mkdir -p ./data/chroma
   chmod 755 ./data/chroma
   ```

### Embedding Issues

#### Problem: Embedding generation fails
```bash
RuntimeError: Failed to generate embeddings
```

**Solutions:**
1. **Check embedding model:**
   ```python
   # Test embedding model
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   embedding = model.encode("test text")
   print(f"Embedding shape: {embedding.shape}")
   ```

2. **Update embedding model:**
   ```bash
   pip install --upgrade sentence-transformers
   ```

3. **Use different embedding model:**
   ```python
   # config/chroma.py
   EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
   ```

### Knowledge Retrieval Issues

#### Problem: Poor search results
```bash
INFO: No relevant context found for query
```

**Diagnostics:**
```bash
# Check knowledge base size
curl http://localhost:8000/api/v1/collections/agent_knowledge

# Test direct query
curl -X POST http://localhost:8000/api/v1/collections/agent_knowledge/query \
  -H "Content-Type: application/json" \
  -d '{"query_texts": ["authentication"], "n_results": 5}'
```

**Solutions:**
1. **Populate knowledge base:**
   ```bash
   uv run python scripts/populate_knowledge_base.py
   ```

2. **Adjust search parameters:**
   ```python
   # Increase search results
   results = await knowledge_base.query(
       query_text, 
       max_results=10,  # Increase from 5
       similarity_threshold=0.6  # Lower from 0.8
   )
   ```

3. **Re-index knowledge base:**
   ```bash
   uv run python scripts/reindex_knowledge_base.py
   ```

## PRP Execution Failures

### Planning Stage Issues

#### Problem: Feature planner fails to generate tasks
```bash
ERROR: Failed to decompose feature into tasks
```

**Diagnostics:**
```bash
# Check planner logs
docker-compose logs planner

# Test LLM connection
python -c "
import openai
client = openai.OpenAI()
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print(response.choices[0].message.content)
"
```

**Solutions:**
1. **Check LLM configuration:**
   ```bash
   # Verify API key
   echo $OPENAI_API_KEY | cut -c1-10
   
   # Test different model
   export OPENAI_MODEL=gpt-3.5-turbo
   ```

2. **Simplify feature specification:**
   ```json
   {
     "title": "Simple Test Feature",
     "description": "Basic functionality test",
     "requirements": ["Single requirement only"]
   }
   ```

3. **Check context limits:**
   ```python
   # Reduce context size
   PLANNER_CONTEXT_SIZE = 2000  # Down from 4000
   ```

### Implementation Issues

#### Problem: Code generation fails
```bash
ERROR: Implementation coder failed to generate code
```

**Solutions:**
1. **Check coder agent logs:**
   ```bash
   docker-compose logs coder
   ```

2. **Verify file system permissions:**
   ```bash
   # Check output directory
   ls -la ./output/
   chmod 755 ./output/
   ```

3. **Test with simple task:**
   ```json
   {
     "title": "Hello World Function",
     "description": "Create a simple hello world function",
     "language": "python"
   }
   ```

### Testing Stage Failures

#### Problem: Tests fail to run
```bash
ERROR: pytest execution failed
```

**Solutions:**
1. **Check test environment:**
   ```bash
   # Run tests manually
   uv run pytest tests/ -v
   
   # Check test dependencies
   pip list | grep pytest
   ```

2. **Verify test configuration:**
   ```python
   # pytest.ini
   [tool:pytest]
   testpaths = tests
   python_files = test_*.py
   python_functions = test_*
   ```

## Performance Issues

### Slow Response Times

#### Problem: API responses taking too long
```bash
WARNING: Request took 30+ seconds to complete
```

**Diagnostics:**
```bash
# Monitor response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8080/agents

# Check system resources
top
htop
docker stats
```

**Solutions:**
1. **Scale agent services:**
   ```yaml
   # docker-compose.yml
   services:
     coder:
       deploy:
         replicas: 3
   ```

2. **Optimize database queries:**
   ```python
   # Add indexes
   CREATE INDEX idx_tasks_status ON tasks(status);
   CREATE INDEX idx_features_created_at ON features(created_at);
   ```

3. **Enable caching:**
   ```python
   # config/cache.py
   REDIS_CACHE_TTL = 3600
   ENABLE_QUERY_CACHE = True
   ```

### Memory Issues

#### Problem: Containers running out of memory
```bash
ERROR: Container killed due to OOM
```

**Solutions:**
1. **Increase memory limits:**
   ```yaml
   # docker-compose.yml
   services:
     coder:
       deploy:
         resources:
           limits:
             memory: 4G
   ```

2. **Monitor memory usage:**
   ```bash
   # Check memory usage
   docker stats --no-stream
   
   # Check for memory leaks
   docker-compose exec coder python -c "
   import psutil
   process = psutil.Process()
   print(f'Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB')
   "
   ```

3. **Optimize agent memory:**
   ```python
   # Clear context periodically
   if len(conversation_history) > 100:
       conversation_history = conversation_history[-50:]
   ```

## Log Analysis

### Reading Agent Logs

#### Key log locations:
```bash
# Container logs
docker-compose logs coordinator
docker-compose logs planner
docker-compose logs coder

# Application logs
tail -f logs/agent-factory.log

# System logs
journalctl -u docker -f
```

#### Important log patterns:

**🔍 Look for these in logs:**

**Error Patterns:**
```bash
# Connection errors
grep -i "connection refused" logs/*
grep -i "timeout" logs/*
grep -i "connection error" logs/*

# Agent errors
grep -i "agent.*error" logs/*
grep -i "task.*failed" logs/*
grep -i "execution.*failed" logs/*

# LLM errors
grep -i "openai.*error" logs/*
grep -i "rate.*limit" logs/*
grep -i "api.*error" logs/*
```

**Performance Patterns:**
```bash
# Slow operations
grep "took.*seconds" logs/*
grep "timeout" logs/*

# Memory issues
grep -i "memory" logs/*
grep -i "oom" logs/*
```

### Log Analysis Tools

#### Centralized logging with ELK stack:
```yaml
# docker-compose.logging.yml
version: '3.8'
services:
  elasticsearch:
    image: elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
      
  logstash:
    image: logstash:7.14.0
    volumes:
      - ./config/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
      
  kibana:
    image: kibana:7.14.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
```

#### Log aggregation script:
```bash
#!/bin/bash
# collect_logs.sh

mkdir -p debug_logs/$(date +%Y%m%d_%H%M%S)
cd debug_logs/$(date +%Y%m%d_%H%M%S)

# Collect system info
docker-compose ps > docker_status.txt
docker stats --no-stream > docker_stats.txt
curl -s http://localhost:8080/health > health_check.json

# Collect agent logs
docker-compose logs coordinator > coordinator.log
docker-compose logs planner > planner.log
docker-compose logs coder > coder.log
docker-compose logs tester > tester.log
docker-compose logs reviewer > reviewer.log
docker-compose logs devops > devops.log

# Collect infrastructure logs
docker-compose logs redis > redis.log
docker-compose logs chroma > chroma.log
docker-compose logs postgres > postgres.log

echo "Logs collected in debug_logs/$(date +%Y%m%d_%H%M%S)/"
```

## Network & Connectivity

### Docker Network Issues

#### Problem: Containers can't reach each other
```bash
curl: (7) Failed to connect to chroma port 8000: Connection refused
```

**Solutions:**
1. **Check Docker network:**
   ```bash
   docker network ls
   docker network inspect agent-factory_default
   ```

2. **Verify service names:**
   ```bash
   # Use service names, not localhost
   # ❌ Wrong: http://localhost:8000
   # ✅ Right: http://chroma:8000
   ```

3. **Test internal connectivity:**
   ```bash
   docker-compose exec api ping chroma
   docker-compose exec api curl http://chroma:8000/api/v1/version
   ```

### External API Issues

#### Problem: LLM API calls failing
```bash
openai.APIConnectionError: Connection error.
```

**Solutions:**
1. **Check internet connectivity:**
   ```bash
   curl -I https://api.openai.com
   ping 8.8.8.8
   ```

2. **Test API credentials:**
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

3. **Check firewall/proxy:**
   ```bash
   # Test with proxy
   export https_proxy=http://your-proxy:8080
   curl https://api.openai.com
   ```

## Database Issues

### PostgreSQL Problems

#### Problem: Database connection fails
```bash
psycopg2.OperationalError: connection to server failed
```

**Solutions:**
1. **Check PostgreSQL status:**
   ```bash
   docker-compose logs postgres
   docker-compose exec postgres pg_isready
   ```

2. **Test connection manually:**
   ```bash
   docker-compose exec postgres psql -U agent_factory -d agent_factory -c "SELECT 1;"
   ```

3. **Check connection string:**
   ```bash
   # Format: postgresql://user:password@host:port/database
   echo $DATABASE_URL
   ```

### Migration Issues

#### Problem: Database schema out of date
```bash
ERROR: relation "features" does not exist
```

**Solutions:**
1. **Run migrations:**
   ```bash
   uv run alembic upgrade head
   ```

2. **Check migration status:**
   ```bash
   uv run alembic current
   uv run alembic history
   ```

3. **Reset database (destructive):**
   ```bash
   docker-compose down postgres
   docker volume rm agent-factory_postgres_data
   docker-compose up -d postgres
   uv run alembic upgrade head
   ```

## Security & Authentication

### API Key Issues

#### Problem: Authentication failures
```bash
401 Unauthorized: Invalid API key
```

**Solutions:**
1. **Generate new API key:**
   ```bash
   curl -X POST http://localhost:8080/auth/api-keys \
     -H "Content-Type: application/json" \
     -d '{"name": "test-key", "permissions": ["features:create"]}'
   ```

2. **Check API key format:**
   ```bash
   # Should be: Bearer sk-...
   curl -H "Authorization: Bearer sk-your-key-here" \
     http://localhost:8080/agents
   ```

### CORS Issues

#### Problem: Browser requests blocked
```bash
Access to fetch at 'http://localhost:8080' blocked by CORS policy
```

**Solutions:**
1. **Update CORS configuration:**
   ```python
   # config/security.py
   CORS_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:8080",
       "https://your-frontend-domain.com"
   ]
   ```

2. **Test CORS headers:**
   ```bash
   curl -H "Origin: http://localhost:3000" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        http://localhost:8080/features
   ```

## FAQ

### General Questions

**Q: How do I reset the entire system?**
```bash
# Complete reset (destructive)
docker-compose down -v
docker system prune -f
docker volume prune -f
rm -rf ./data/
git clean -fdx
docker-compose up -d
uv run python scripts/init_system.py
```

**Q: How do I upgrade to a new version?**
```bash
# Safe upgrade process
git stash
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
uv run alembic upgrade head
```

**Q: How do I backup my data?**
```bash
# Backup script
mkdir -p backups/$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U agent_factory agent_factory > backups/$(date +%Y%m%d_%H%M%S)/postgres.sql
cp -r ./data/chroma backups/$(date +%Y%m%d_%H%M%S)/
```

### Performance Questions

**Q: Why are features taking so long to complete?**

Common causes:
1. **Insufficient agent resources** - Scale up coder instances
2. **LLM rate limiting** - Check API quotas
3. **Complex feature specification** - Break down into smaller tasks
4. **Knowledge base performance** - Optimize vector database
5. **Network latency** - Check connectivity to external APIs

**Q: How do I optimize for cost?**
```python
# Use cheaper models for simpler tasks
AGENT_MODELS = {
    "planner": "gpt-4-turbo-preview",  # Complex planning
    "coder": "gpt-3.5-turbo",         # Code generation
    "reviewer": "gpt-3.5-turbo",      # Code review
    "tester": "gpt-3.5-turbo"        # Test generation
}
```

### Development Questions

**Q: How do I add a custom agent?**
1. Create agent class inheriting from `BaseAgent`
2. Implement required methods (`_execute_prp`, `_execute_task_impl`)
3. Add agent configuration to `config/agents/`
4. Add agent to Docker Compose services
5. Register agent with coordinator

**Q: How do I debug agent behavior?**
```python
# Enable debug logging
import logging
logging.getLogger('agent_factory').setLevel(logging.DEBUG)

# Add debug prints in agent code
logger.debug(f"Processing task: {task.title}")
logger.debug(f"Context retrieved: {len(context)} entries")
```

### Troubleshooting Last Resort

**Q: Nothing works, what should I do?**

1. **Collect debug information:**
   ```bash
   bash scripts/collect_debug_info.sh
   ```

2. **Check system requirements:**
   - Python 3.12+
   - Docker & Docker Compose
   - 8GB+ RAM available
   - 10GB+ disk space
   - Internet connectivity

3. **Try minimal setup:**
   ```bash
   # Start with just core services
   docker-compose up -d redis postgres chroma
   # Test each service individually
   ```

4. **Contact support:**
   - Include debug logs
   - Describe steps to reproduce
   - Mention your environment (OS, Docker version, Python version)
   - Check GitHub issues for similar problems

---

## Getting Additional Help

### Resources
- **Documentation**: [docs/index.md](index.md)
- **Configuration Guide**: [CONFIGURATION.md](CONFIGURATION.md)
- **Architecture Guide**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **GitHub Issues**: Submit bug reports and feature requests

### Debug Commands Reference
```bash
# Quick health check
curl http://localhost:8080/health | jq

# Comprehensive status
bash scripts/system_status.sh

# Collect debug logs
bash scripts/collect_logs.sh

# Validate configuration
python scripts/validate_config.py

# Test all connections
python scripts/test_connections.py
```

Remember: Most issues are configuration-related. Always check environment variables, network connectivity, and service status first! 🔧
