#!/usr/bin/env python3
"""
Knowledge Base Update Script
Updates the vector store with all project documentation and configurations.
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any
import sys
import os

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from knowledge.vector_store.chroma_client import ChromaVectorStore
from models.base import KnowledgeEntry
from pydantic import BaseModel

class Document(BaseModel):
    """Document model for knowledge base updates."""
    content: str
    metadata: Dict[str, Any]
    doc_id: str

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeBaseUpdater:
    """Updates the knowledge base with project documentation."""
    
    def __init__(self):
        self.vector_store = ChromaVectorStore()
        self.project_root = Path(__file__).parent.parent
        
    async def initialize(self):
        """Initialize the vector store connection."""
        logger.info("Initializing vector store connection...")
        # Vector store should auto-initialize
        
    def get_documentation_files(self) -> List[Path]:
        """Get all documentation files to index."""
        doc_patterns = [
            # Main documentation
            "README.md",
            "QUICKSTART.md", 
            "ONBOARDING.md",
            "AGENTS.md",
            "CLAUDE.md",
            "CLAUDE.local.md",
            "DEPLOYMENT.md",
            "PROJECT_PROGRESS.md",
            
            # Docs directory
            "docs/*.md",
            
            # Claude commands (important for AI agents)
            ".claude/commands/**/*.md",
            
            # Cursor rules
            ".cursor/rules/*.md",
            
            # Agent configurations
            ".claude/agents/*.md",
            
            # PRP templates and documentation
            "PRPs/README.md",
            "PRPs/templates/*.md",
            "PRPs/ai_docs/*.md",
            
            # Configuration examples
            ".env.example",
            "pyproject.toml",
        ]
        
        files = []
        for pattern in doc_patterns:
            if "*" in pattern:
                files.extend(self.project_root.glob(pattern))
            else:
                file_path = self.project_root / pattern
                if file_path.exists():
                    files.append(file_path)
                    
        # Filter for existing files and remove duplicates
        return list(set(f for f in files if f.exists() and f.is_file()))
    
    def create_document(self, file_path: Path) -> Document:
        """Create a Document object from a file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Determine document type and metadata
            doc_type = self.get_document_type(file_path)
            relative_path = file_path.relative_to(self.project_root)
            
            metadata = {
                "file_path": str(relative_path),
                "file_name": file_path.name,
                "doc_type": doc_type,
                "size": len(content),
                "last_updated": "2025-01-28",  # Current update
            }
            
            # Add specific metadata based on file type
            if file_path.name.endswith('.md'):
                metadata["format"] = "markdown"
                # Extract title from first heading if available
                lines = content.split('\n')
                for line in lines[:10]:  # Check first 10 lines
                    if line.startswith('# '):
                        metadata["title"] = line[2:].strip()
                        break
                        
            return Document(
                content=content,
                metadata=metadata,
                doc_id=str(relative_path)
            )
            
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None
    
    def get_document_type(self, file_path: Path) -> str:
        """Determine the document type based on file path."""
        path_str = str(file_path)
        
        if "/.claude/commands/" in path_str:
            return "claude_command"
        elif "/.claude/agents/" in path_str:
            return "agent_config"
        elif "/.cursor/rules/" in path_str:
            return "cursor_rule"
        elif "/docs/" in path_str:
            return "documentation"
        elif "/PRPs/" in path_str:
            return "prp_template"
        elif file_path.name in ["README.md", "QUICKSTART.md", "ONBOARDING.md"]:
            return "main_documentation"
        elif file_path.name.endswith('.md'):
            return "markdown_doc"
        elif file_path.name in ["pyproject.toml", ".env.example"]:
            return "configuration"
        else:
            return "other"
    
    async def update_knowledge_base(self):
        """Update the knowledge base with all documentation."""
        logger.info("Starting knowledge base update...")
        
        # Get all documentation files
        doc_files = self.get_documentation_files()
        logger.info(f"Found {len(doc_files)} documentation files to index")
        
        # Process files in batches
        batch_size = 10
        total_indexed = 0
        
        for i in range(0, len(doc_files), batch_size):
            batch = doc_files[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(doc_files) + batch_size - 1)//batch_size}")
            
            documents = []
            for file_path in batch:
                doc = self.create_document(file_path)
                if doc:
                    documents.append(doc)
                    logger.info(f"  Prepared: {file_path.relative_to(self.project_root)}")
            
            # Store documents in vector store
            if documents:
                try:
                    for doc in documents:
                        # Convert Document to KnowledgeEntry
                        knowledge_entry = KnowledgeEntry(
                            content=doc.content,
                            source_type=doc.metadata.get("doc_type", "documentation"),
                            metadata=doc.metadata
                        )
                        await self.vector_store.store_knowledge(knowledge_entry)
                    
                    total_indexed += len(documents)
                    logger.info(f"  Indexed {len(documents)} documents")
                except Exception as e:
                    logger.error(f"Error indexing batch: {e}")
            
            # Small delay between batches
            await asyncio.sleep(0.5)
        
        logger.info(f"Knowledge base update complete! Indexed {total_indexed} documents")
        
    async def verify_indexing(self):
        """Verify that documents were properly indexed."""
        logger.info("Verifying knowledge base indexing...")
        
        # Test queries to verify different document types
        test_queries = [
            "quick start guide setup",
            "agent configuration",
            "claude commands",
            "development workflow",
            "project structure"
        ]
        
        for query in test_queries:
            try:
                results = await self.vector_store.query_similar(query, n_results=3)
                logger.info(f"Query '{query}': Found {len(results)} results")
                for result in results[:2]:  # Show top 2 results
                    metadata = result.metadata if hasattr(result, 'metadata') else {}
                    logger.info(f"  - {metadata.get('file_path', 'unknown')} ({metadata.get('doc_type', 'unknown')})")
            except Exception as e:
                logger.error(f"Error querying '{query}': {e}")

async def main():
    """Main function to update knowledge base."""
    updater = KnowledgeBaseUpdater()
    
    try:
        await updater.initialize()
        await updater.update_knowledge_base()
        await updater.verify_indexing()
        
    except Exception as e:
        logger.error(f"Knowledge base update failed: {e}")
        sys.exit(1)
    
    logger.info("Knowledge base update completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
