#!/usr/bin/env python3
"""Comprehensive deployment script for Agent Factory system."""

import asyncio
import logging
import os
import sys
import time
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
DOCKER_COMPOSE_FILE = "docker-compose.yml"
API_BASE_URL = "http://localhost:8000"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
CHROMA_URL = "http://localhost:8001"
REDIS_URL = "http://localhost:6379"

# Service dependencies and startup order
SERVICES = [
    "redis",
    "chromadb", 
    "agent-api",
    "agent-coordinator",
    "agent-planner",
    "agent-coder",
    "agent-tester",
    "agent-reviewer",
    "agent-devops"
]

# Health check timeouts
HEALTH_CHECK_TIMEOUT = 30  # seconds
SERVICE_STARTUP_TIMEOUT = 60  # seconds


class SystemDeployer:
    """Deploy and manage the Agent Factory system."""
    
    def __init__(self):
        """Initialize the deployer."""
        self.deployment_status: Dict[str, str] = {}
        self.health_status: Dict[str, str] = {}
        
    async def deploy_system(self) -> bool:
        """Deploy the entire system."""
        logger.info("🚀 Starting Agent Factory system deployment...")
        
        try:
            # Check prerequisites
            if not await self._check_prerequisites():
                logger.error("❌ Prerequisites not met. Deployment failed.")
                return False
            
            # Start infrastructure services
            logger.info("🏗️ Starting infrastructure services...")
            if not await self._start_infrastructure():
                logger.error("❌ Infrastructure startup failed. Deployment failed.")
                return False
            
            # Start agent services
            logger.info("🤖 Starting agent services...")
            if not await self._start_agents():
                logger.error("❌ Agent startup failed. Deployment failed.")
                return False
            
            # Verify system health
            logger.info("🔍 Verifying system health...")
            if not await self._verify_system_health():
                logger.error("❌ System health verification failed.")
                return False
            
            logger.info("🎉 System deployment completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"💥 Deployment failed with error: {e}")
            return False
    
    async def _check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        logger.info("🔍 Checking prerequisites...")
        
        # Check Docker
        if not self._check_docker():
            logger.error("❌ Docker is not running or not accessible")
            return False
        
        # Check Docker Compose
        if not self._check_docker_compose():
            logger.error("❌ Docker Compose is not accessible")
            return False
        
        # Check if docker-compose.yml exists
        if not Path(DOCKER_COMPOSE_FILE).exists():
            logger.error(f"❌ {DOCKER_COMPOSE_FILE} not found")
            return False
        
        # Check ports availability
        if not await self._check_ports_available():
            logger.error("❌ Required ports are not available")
            return False
        
        logger.info("✅ Prerequisites check passed")
        return True
    
    def _check_docker(self) -> bool:
        """Check if Docker is running."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _check_docker_compose(self) -> bool:
        """Check if Docker Compose is accessible."""
        try:
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    async def _check_ports_available(self) -> bool:
        """Check if required ports are available."""
        import socket
        
        ports_to_check = [8000, 8001, 6379]
        
        for port in ports_to_check:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(('localhost', port))
                    if result == 0:
                        logger.warning(f"⚠️ Port {port} is already in use")
                        # Don't fail for now, just warn
            except Exception as e:
                logger.debug(f"Port {port} check: {e}")
        
        return True
    
    async def _start_infrastructure(self) -> bool:
        """Start infrastructure services (Redis, ChromaDB)."""
        logger.info("🏗️ Starting infrastructure services...")
        
        try:
            # Start Redis and ChromaDB
            result = subprocess.run([
                "docker-compose", "-f", DOCKER_COMPOSE_FILE,
                "up", "-d", "redis", "chromadb"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.error(f"❌ Failed to start infrastructure: {result.stderr}")
                return False
            
            # Wait for services to be healthy
            logger.info("⏳ Waiting for infrastructure services to be healthy...")
            if not await self._wait_for_infrastructure_health():
                logger.error("❌ Infrastructure services failed health checks")
                return False
            
            logger.info("✅ Infrastructure services started successfully")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("❌ Infrastructure startup timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Infrastructure startup failed: {e}")
            return False
    
    async def _wait_for_infrastructure_health(self) -> bool:
        """Wait for infrastructure services to be healthy."""
        start_time = time.time()
        
        while time.time() - start_time < SERVICE_STARTUP_TIMEOUT:
            try:
                # Check Redis
                redis_healthy = await self._check_redis_health()
                
                # Check ChromaDB
                chroma_healthy = await self._check_chroma_health()
                
                if redis_healthy and chroma_healthy:
                    logger.info("✅ Infrastructure services are healthy")
                    return True
                
                logger.info("⏳ Waiting for infrastructure services...")
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.debug(f"Health check error: {e}")
                await asyncio.sleep(5)
        
        logger.error("❌ Infrastructure health check timeout")
        return False
    
    async def _check_redis_health(self) -> bool:
        """Check Redis health."""
        try:
            # Try to connect to Redis
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=5)
            r.ping()
            return True
        except Exception:
            return False
    
    async def _check_chroma_health(self) -> bool:
        """Check ChromaDB health."""
        try:
            response = requests.get(f"{CHROMA_URL}/api/v1/heartbeat", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    async def _start_agents(self) -> bool:
        """Start agent services."""
        logger.info("🤖 Starting agent services...")
        
        try:
            # Start all agent services
            result = subprocess.run([
                "docker-compose", "-f", DOCKER_COMPOSE_FILE,
                "up", "-d", "agent-coordinator", "agent-planner", 
                "agent-coder", "agent-tester", "agent-reviewer", "agent-devops"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                logger.error(f"❌ Failed to start agents: {result.stderr}")
                return False
            
            # Wait for agents to be healthy
            logger.info("⏳ Waiting for agents to be healthy...")
            if not await self._wait_for_agents_health():
                logger.error("❌ Agents failed health checks")
                return False
            
            logger.info("✅ Agent services started successfully")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("❌ Agent startup timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Agent startup failed: {e}")
            return False
    
    async def _wait_for_agents_health(self) -> bool:
        """Wait for agents to be healthy."""
        start_time = time.time()
        
        while time.time() - start_time < SERVICE_STARTUP_TIMEOUT:
            try:
                # Check API health
                response = requests.get(f"{HEALTH_ENDPOINT}/agents", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    total_agents = data.get("total_agents", 0)
                    healthy_agents = data.get("healthy_agents", 0)
                    
                    if healthy_agents > 0:  # At least some agents are healthy
                        logger.info(f"✅ {healthy_agents}/{total_agents} agents are healthy")
                        return True
                
                logger.info("⏳ Waiting for agents to be healthy...")
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.debug(f"Agent health check error: {e}")
                await asyncio.sleep(10)
        
        logger.error("❌ Agent health check timeout")
        return False
    
    async def _verify_system_health(self) -> bool:
        """Verify overall system health."""
        logger.info("🔍 Verifying system health...")
        
        try:
            # Check system status
            response = requests.get(f"{HEALTH_ENDPOINT}/status", timeout=10)
            if response.status_code != 200:
                logger.error(f"❌ System status check failed: {response.status_code}")
                return False
            
            data = response.json()
            overall_status = data.get("system", {}).get("overall", {}).get("status", "unknown")
            
            if overall_status in ["healthy", "warning"]:
                logger.info(f"✅ System is {overall_status}")
                return True
            else:
                logger.error(f"❌ System is {overall_status}")
                return False
                
        except Exception as e:
            logger.error(f"❌ System health verification failed: {e}")
            return False
    
    async def get_system_status(self) -> Dict:
        """Get current system status."""
        try:
            response = requests.get(f"{HEALTH_ENDPOINT}/status", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status check failed: {response.status_code}"}
        except Exception as e:
            return {"error": f"Status check failed: {e}"}
    
    async def stop_system(self) -> bool:
        """Stop the entire system."""
        logger.info("🛑 Stopping Agent Factory system...")
        
        try:
            result = subprocess.run([
                "docker-compose", "-f", DOCKER_COMPOSE_FILE, "down"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ System stopped successfully")
                return True
            else:
                logger.error(f"❌ Failed to stop system: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ System stop failed: {e}")
            return False
    
    async def restart_system(self) -> bool:
        """Restart the entire system."""
        logger.info("🔄 Restarting Agent Factory system...")
        
        if await self.stop_system():
            await asyncio.sleep(5)  # Wait for cleanup
            return await self.deploy_system()
        else:
            return False


async def main():
    """Main deployment function."""
    deployer = SystemDeployer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "deploy":
            success = await deployer.deploy_system()
            sys.exit(0 if success else 1)
            
        elif command == "stop":
            success = await deployer.stop_system()
            sys.exit(0 if success else 1)
            
        elif command == "restart":
            success = await deployer.restart_system()
            sys.exit(0 if success else 1)
            
        elif command == "status":
            status = await deployer.get_system_status()
            print(json.dumps(status, indent=2))
            sys.exit(0)
            
        else:
            print(f"Unknown command: {command}")
            print("Available commands: deploy, stop, restart, status")
            sys.exit(1)
    else:
        # Default: deploy the system
        success = await deployer.deploy_system()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)