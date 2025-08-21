#!/usr/bin/env python3
"""Main entry point for planner agent."""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

from communication.message_bus import RedisMessageBus
from knowledge.vector_store import ChromaVectorStore
from agents.planner import FeaturePlanner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    """Main entry point for planner agent."""
    try:
        # Initialize Redis connection
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_db = int(os.getenv("REDIS_DB", "0"))
        redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
        
        message_bus = RedisMessageBus(redis_url=redis_url)
        await message_bus.connect()
        
        # Initialize ChromaDB connection
        chroma_host = os.getenv("CHROMA_HOST", "localhost")
        chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
        chroma_url = f"http://{chroma_host}:{chroma_port}"
        
        knowledge_base = ChromaVectorStore(chroma_url=chroma_url)
        await knowledge_base.connect()
        
        # Create and start planner agent
        planner = FeaturePlanner(
            knowledge_base=knowledge_base,
            message_bus=message_bus,
        )
        
        logger.info("Starting Feature Planner Agent...")
        await planner.start()
        
        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
        finally:
            await planner.stop()
            await knowledge_base.disconnect()
            await message_bus.disconnect()
            
    except Exception as e:
        logger.error(f"Error running planner agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
