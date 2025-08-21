#!/usr/bin/env python3
"""
Simple Knowledge Base Update Script
Uses the existing API to update the knowledge base with documentation.
"""

import asyncio
import logging
import json
from pathlib import Path
import aiohttp
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleKnowledgeUpdater:
    """Simple knowledge base updater using the REST API."""
    
    def __init__(self, api_base_url: str = "http://localhost:8080"):
        self.api_base_url = api_base_url
        self.project_root = Path(__file__).parent.parent
        
    def get_documentation_files(self) -> list[Path]:
        """Get all documentation files to index."""
        doc_patterns = [
            # Main documentation
            "README.md",
            "QUICKSTART.md", 
            "ONBOARDING.md",
            "AGENTS.md",
            "CLAUDE.md",
            "DEPLOYMENT.md",
            
            # Docs directory
            "docs/SHARED_COMPONENTS.md",
            "docs/PROJECT_STRUCTURE.md",
            "docs/API_REFERENCE.md",
            "docs/ARCHITECTURE.md",
            "docs/USER_GUIDE.md",
            "docs/DEVELOPER_REFERENCE.md",
            "docs/CONFIGURATION.md",
            "docs/TROUBLESHOOTING.md",
            
            # Claude commands (important for AI agents)
            ".claude/commands/prp-commands/prp-base-create.md",
            ".claude/commands/prp-commands/prp-base-execute.md",
            ".claude/commands/development/prime-core.md",
            ".claude/commands/code-quality/review-staged-unstaged.md",
            
            # Agent configurations
            ".claude/agents/seo-analyzer.md",
            ".claude/agents/seo-collector.md", 
            ".claude/agents/seo-processor.md",
            
            # PRP documentation
            "PRPs/README.md",
        ]
        
        files = []
        for pattern in doc_patterns:
            file_path = self.project_root / pattern
            if file_path.exists():
                files.append(file_path)
                
        return files
    
    def get_document_type(self, file_path: Path) -> str:
        """Determine the document type based on file path."""
        path_str = str(file_path)
        
        if "/.claude/commands/" in path_str:
            return "claude_command"
        elif "/.claude/agents/" in path_str:
            return "agent_config"
        elif "/docs/" in path_str:
            return "documentation"
        elif "/PRPs/" in path_str:
            return "prp_template"
        elif file_path.name in ["README.md", "QUICKSTART.md", "ONBOARDING.md"]:
            return "main_documentation"
        else:
            return "markdown_doc"
    
    async def store_document(self, session: aiohttp.ClientSession, file_path: Path) -> bool:
        """Store a single document via the API."""
        try:
            content = file_path.read_text(encoding='utf-8')
            relative_path = file_path.relative_to(self.project_root)
            
            # Prepare the knowledge entry
            knowledge_data = {
                "content": content,
                "source_type": self.get_document_type(file_path),
                "metadata": {
                    "file_path": str(relative_path),
                    "file_name": file_path.name,
                    "doc_type": self.get_document_type(file_path),
                    "size": len(content),
                    "last_updated": "2025-01-28",
                }
            }
            
            # Extract title from markdown if available
            if file_path.name.endswith('.md'):
                lines = content.split('\n')
                for line in lines[:10]:
                    if line.startswith('# '):
                        knowledge_data["metadata"]["title"] = line[2:].strip()
                        break
            
            # Store via API
            async with session.post(
                f"{self.api_base_url}/knowledge/store",
                json=knowledge_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    logger.info(f"✅ Stored: {relative_path}")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Failed to store {relative_path}: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error processing {file_path}: {e}")
            return False
    
    async def wait_for_api(self, max_retries: int = 30) -> bool:
        """Wait for the API to be ready."""
        logger.info("Waiting for API to be ready...")
        
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.api_base_url}/health") as response:
                        if response.status == 200:
                            logger.info("✅ API is ready!")
                            return True
            except Exception:
                pass
            
            logger.info(f"API not ready, attempt {attempt + 1}/{max_retries}...")
            await asyncio.sleep(2)
        
        logger.error("❌ API failed to become ready")
        return False
    
    async def update_knowledge_base(self):
        """Update the knowledge base with all documentation."""
        logger.info("🚀 Starting knowledge base update...")
        
        # Wait for API to be ready
        if not await self.wait_for_api():
            return False
        
        # Get all documentation files
        doc_files = self.get_documentation_files()
        logger.info(f"📚 Found {len(doc_files)} documentation files to index")
        
        # Process files
        successful = 0
        failed = 0
        
        async with aiohttp.ClientSession() as session:
            for file_path in doc_files:
                if await self.store_document(session, file_path):
                    successful += 1
                else:
                    failed += 1
                
                # Small delay between requests
                await asyncio.sleep(0.2)
        
        logger.info(f"📊 Knowledge base update complete!")
        logger.info(f"   ✅ Successfully indexed: {successful} documents")
        logger.info(f"   ❌ Failed: {failed} documents")
        
        return successful > 0
    
    async def verify_indexing(self):
        """Verify that documents were properly indexed."""
        logger.info("🔍 Verifying knowledge base indexing...")
        
        test_queries = [
            "quick start guide setup",
            "agent configuration", 
            "claude commands",
            "development workflow",
            "project structure"
        ]
        
        async with aiohttp.ClientSession() as session:
            for query in test_queries:
                try:
                    async with session.post(
                        f"{self.api_base_url}/knowledge/query",
                        json={"query": query, "limit": 3},
                        headers={"Content-Type": "application/json"}
                    ) as response:
                        if response.status == 200:
                            results = await response.json()
                            logger.info(f"Query '{query}': Found {len(results)} results")
                            for result in results[:2]:
                                metadata = result.get('metadata', {})
                                file_path = metadata.get('file_path', 'unknown')
                                doc_type = metadata.get('doc_type', 'unknown')
                                logger.info(f"  - {file_path} ({doc_type})")
                        else:
                            logger.error(f"Query '{query}' failed: {response.status}")
                except Exception as e:
                    logger.error(f"Error querying '{query}': {e}")

async def main():
    """Main function to update knowledge base."""
    updater = SimpleKnowledgeUpdater()
    
    try:
        success = await updater.update_knowledge_base()
        if success:
            await updater.verify_indexing()
            logger.info("🎉 Knowledge base update completed successfully!")
        else:
            logger.error("❌ Knowledge base update failed!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Knowledge base update failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
