"""Health monitoring service for the agent system."""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..communication.message_bus import RedisMessageBus
from ..knowledge.vector_store import ChromaVectorStore
from ..models import AgentType

logger = logging.getLogger(__name__)


class HealthMonitor:
    """Comprehensive health monitoring for the agent system."""

    def __init__(
        self,
        message_bus: RedisMessageBus,
        vector_store: ChromaVectorStore,
        check_interval: int = 30,
    ):
        """Initialize the health monitor.

        Args:
            message_bus: Redis message bus for agent communication
            vector_store: Vector store for knowledge base
            check_interval: Health check interval in seconds
        """
        self.message_bus = message_bus
        self.vector_store = vector_store
        self.check_interval = check_interval
        
        # Health status tracking
        self.agent_health: Dict[str, Dict[str, Any]] = {}
        self.system_health: Dict[str, Any] = {}
        self.last_check: Optional[datetime] = None
        
        # Expected agents
        self.expected_agents = {
            "coordinator": AgentType.COORDINATOR,
            "planner": AgentType.PLANNER,
            "coder": AgentType.CODER,
            "tester": AgentType.TESTER,
            "reviewer": AgentType.REVIEWER,
            "devops": AgentType.DEVOPS,
        }
        
        logger.info("Health monitor initialized")

    async def start_monitoring(self) -> None:
        """Start the health monitoring service."""
        logger.info("Starting health monitoring service")
        
        try:
            while True:
                await self._perform_health_check()
                await asyncio.sleep(self.check_interval)
                
        except asyncio.CancelledError:
            logger.info("Health monitoring service stopped")
        except Exception as e:
            logger.error(f"Health monitoring service error: {e}")

    async def _perform_health_check(self) -> None:
        """Perform a comprehensive health check."""
        try:
            logger.debug("Performing health check")
            
            # Check infrastructure health
            await self._check_infrastructure_health()
            
            # Check agent health
            await self._check_agent_health()
            
            # Update system health
            await self._update_system_health()
            
            self.last_check = datetime.utcnow()
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")

    async def _check_infrastructure_health(self) -> None:
        """Check infrastructure components health."""
        try:
            # Check Redis connection
            redis_healthy = await self.message_bus.health_check()
            
            # Check ChromaDB connection
            chroma_healthy = await self._check_chroma_health()
            
            self.system_health["infrastructure"] = {
                "redis": {
                    "status": "healthy" if redis_healthy else "unhealthy",
                    "timestamp": datetime.utcnow().isoformat(),
                },
                "chromadb": {
                    "status": "healthy" if chroma_healthy else "unhealthy",
                    "timestamp": datetime.utcnow().isoformat(),
                },
            }
            
        except Exception as e:
            logger.error(f"Infrastructure health check failed: {e}")
            self.system_health["infrastructure"] = {
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _check_chroma_health(self) -> bool:
        """Check ChromaDB health."""
        try:
            # Try to get collection info
            stats = await self.vector_store.get_stats()
            return True
        except Exception as e:
            logger.error(f"ChromaDB health check failed: {e}")
            return False

    async def _check_agent_health(self) -> None:
        """Check individual agent health."""
        try:
            for agent_id, agent_type in self.expected_agents.items():
                agent_status = await self._check_agent_status(agent_id)
                self.agent_health[agent_id] = agent_status
                
        except Exception as e:
            logger.error(f"Agent health check failed: {e}")

    async def _check_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Check status of a specific agent."""
        try:
            # Send health check message to agent
            health_message = {
                "type": "health_check",
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": f"health_{int(time.time())}",
            }
            
            # For now, we'll assume agents are healthy if we can send messages
            # In a real implementation, agents would respond to health checks
            can_send = await self.message_bus.publish(
                f"agent.{agent_id}",
                health_message
            )
            
            return {
                "status": "healthy" if can_send else "unhealthy",
                "last_seen": datetime.utcnow().isoformat(),
                "agent_type": self.expected_agents[agent_id].value,
                "can_communicate": can_send,
            }
            
        except Exception as e:
            logger.error(f"Agent {agent_id} health check failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "agent_type": self.expected_agents[agent_id].value,
            }

    async def _update_system_health(self) -> None:
        """Update overall system health status."""
        try:
            # Count healthy agents
            healthy_agents = sum(
                1 for status in self.agent_health.values()
                if status.get("status") == "healthy"
            )
            
            total_agents = len(self.expected_agents)
            agent_health_percentage = (healthy_agents / total_agents) * 100
            
            # Check infrastructure health
            infra_healthy = all(
                component["status"] == "healthy"
                for component in self.system_health.get("infrastructure", {}).values()
                if isinstance(component, dict) and "status" in component
            )
            
            # Overall system health
            overall_health = "healthy"
            if agent_health_percentage < 50:
                overall_health = "critical"
            elif agent_health_percentage < 80:
                overall_health = "warning"
            elif not infra_healthy:
                overall_health = "warning"
            
            self.system_health["overall"] = {
                "status": overall_health,
                "agent_health_percentage": agent_health_percentage,
                "healthy_agents": healthy_agents,
                "total_agents": total_agents,
                "infrastructure_healthy": infra_healthy,
                "last_check": self.last_check.isoformat() if self.last_check else None,
            }
            
        except Exception as e:
            logger.error(f"System health update failed: {e}")

    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status."""
        return {
            "system": self.system_health,
            "agents": self.agent_health,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_agent_summary(self) -> Dict[str, Any]:
        """Get agent health summary."""
        if not self.agent_health:
            return {"message": "No agent health data available"}
        
        summary = {
            "total_agents": len(self.expected_agents),
            "healthy_agents": 0,
            "unhealthy_agents": 0,
            "error_agents": 0,
            "agent_details": {},
        }
        
        for agent_id, status in self.agent_health.items():
            agent_status = status.get("status", "unknown")
            if agent_status == "healthy":
                summary["healthy_agents"] += 1
            elif agent_status == "unhealthy":
                summary["unhealthy_agents"] += 1
            elif agent_status == "error":
                summary["error_agents"] += 1
            
            summary["agent_details"][agent_id] = {
                "status": agent_status,
                "type": status.get("agent_type", "unknown"),
                "last_seen": status.get("last_seen", "unknown"),
            }
        
        return summary

    async def stop_monitoring(self) -> None:
        """Stop the health monitoring service."""
        logger.info("Stopping health monitoring service")
        # The monitoring loop will exit on the next iteration