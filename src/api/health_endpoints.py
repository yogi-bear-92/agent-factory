"""Health monitoring API endpoints."""

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from .health_monitor import HealthMonitor
from ..communication.message_bus import RedisMessageBus
from ..knowledge.vector_store import ChromaVectorStore

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


async def get_health_monitor() -> HealthMonitor:
    """Dependency to get health monitor instance."""
    # In a real implementation, this would be a singleton or from app state
    message_bus = RedisMessageBus()
    vector_store = ChromaVectorStore()
    return HealthMonitor(message_bus, vector_store)


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "agent-factory",
        "timestamp": "2025-01-27T00:00:00Z"
    }


@router.get("/status")
async def get_system_status(health_monitor: HealthMonitor = Depends(get_health_monitor)) -> Dict[str, Any]:
    """Get comprehensive system health status."""
    try:
        status = health_monitor.get_health_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")


@router.get("/agents")
async def get_agent_summary(health_monitor: HealthMonitor = Depends(get_health_monitor)) -> Dict[str, Any]:
    """Get agent health summary."""
    try:
        summary = health_monitor.get_agent_summary()
        return summary
    except Exception as e:
        logger.error(f"Failed to get agent summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent summary: {str(e)}")


@router.get("/agents/{agent_id}")
async def get_agent_status(
    agent_id: str,
    health_monitor: HealthMonitor = Depends(get_health_monitor)
) -> Dict[str, Any]:
    """Get status of a specific agent."""
    try:
        status = health_monitor.get_health_status()
        agent_status = status.get("agents", {}).get(agent_id)
        
        if not agent_status:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        return {
            "agent_id": agent_id,
            "status": agent_status
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent {agent_id} status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")


@router.get("/infrastructure")
async def get_infrastructure_status(health_monitor: HealthMonitor = Depends(get_health_monitor)) -> Dict[str, Any]:
    """Get infrastructure health status."""
    try:
        status = health_monitor.get_health_status()
        infra_status = status.get("system", {}).get("infrastructure", {})
        
        return {
            "infrastructure": infra_status,
            "timestamp": status.get("timestamp")
        }
    except Exception as e:
        logger.error(f"Failed to get infrastructure status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get infrastructure status: {str(e)}")


@router.post("/agents/{agent_id}/ping")
async def ping_agent(
    agent_id: str,
    health_monitor: HealthMonitor = Depends(get_health_monitor)
) -> Dict[str, Any]:
    """Send a ping to a specific agent."""
    try:
        # This would trigger an immediate health check for the agent
        # For now, return the current status
        status = health_monitor.get_health_status()
        agent_status = status.get("agents", {}).get(agent_id)
        
        if not agent_status:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        return {
            "agent_id": agent_id,
            "ping_sent": True,
            "current_status": agent_status,
            "timestamp": status.get("timestamp")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to ping agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to ping agent: {str(e)}")


@router.get("/metrics")
async def get_system_metrics(health_monitor: HealthMonitor = Depends(get_health_monitor)) -> Dict[str, Any]:
    """Get system performance metrics."""
    try:
        status = health_monitor.get_health_status()
        
        # Calculate metrics
        agents = status.get("agents", {})
        total_agents = len(agents)
        healthy_agents = sum(1 for a in agents.values() if a.get("status") == "healthy")
        unhealthy_agents = sum(1 for a in agents.values() if a.get("status") == "unhealthy")
        error_agents = sum(1 for a in agents.values() if a.get("status") == "error")
        
        # Infrastructure health
        infra = status.get("system", {}).get("infrastructure", {})
        infra_healthy = all(
            component.get("status") == "healthy"
            for component in infra.values()
            if isinstance(component, dict) and "status" in component
        )
        
        metrics = {
            "agents": {
                "total": total_agents,
                "healthy": healthy_agents,
                "unhealthy": unhealthy_agents,
                "error": error_agents,
                "health_percentage": (healthy_agents / total_agents * 100) if total_agents > 0 else 0
            },
            "infrastructure": {
                "overall_health": "healthy" if infra_healthy else "unhealthy",
                "components": {
                    name: comp.get("status", "unknown")
                    for name, comp in infra.items()
                    if isinstance(comp, dict) and "status" in comp
                }
            },
            "system": {
                "overall_status": status.get("system", {}).get("overall", {}).get("status", "unknown"),
                "last_check": status.get("timestamp")
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get system metrics: {str(e)}")


@router.get("/ready")
async def readiness_check(health_monitor: HealthMonitor = Depends(get_health_monitor)) -> Dict[str, Any]:
    """Readiness check for Kubernetes/load balancer health checks."""
    try:
        status = health_monitor.get_health_status()
        
        # Check if system is ready
        overall_status = status.get("system", {}).get("overall", {}).get("status", "unknown")
        is_ready = overall_status in ["healthy", "warning"]  # Allow warning as ready
        
        if is_ready:
            return {
                "ready": True,
                "status": overall_status,
                "timestamp": status.get("timestamp")
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "ready": False,
                    "status": overall_status,
                    "timestamp": status.get("timestamp"),
                    "message": "System not ready"
                }
            )
            
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "ready": False,
                "status": "error",
                "timestamp": "2025-01-27T00:00:00Z",
                "message": f"Readiness check failed: {str(e)}"
            }
        )


@router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes health checks."""
    return {
        "alive": True,
        "timestamp": "2025-01-27T00:00:00Z"
    }