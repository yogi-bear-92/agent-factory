#!/usr/bin/env python3
"""
Direct Knowledge Base Update Script
Directly updates ChromaDB with documentation without using the API.
"""

import logging
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DirectKnowledgeUpdater:
    """Direct knowledge base updater using ChromaDB."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.persist_directory = "./data/chroma"
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="agent_knowledge",
            metadata={"description": "Agent knowledge base"}
        )
        
        logger.info("✅ Initialized ChromaDB connection")
        
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
    
    def store_document(self, file_path: Path) -> bool:
        """Store a single document in ChromaDB."""
        try:
            content = file_path.read_text(encoding='utf-8')
            relative_path = file_path.relative_to(self.project_root)
            
            # Create metadata
            metadata = {
                "file_path": str(relative_path),
                "file_name": file_path.name,
                "doc_type": self.get_document_type(file_path),
                "size": len(content),
                "last_updated": "2025-01-28",
            }
            
            # Extract title from markdown if available
            if file_path.name.endswith('.md'):
                lines = content.split('\n')
                for line in lines[:10]:
                    if line.startswith('# '):
                        metadata["title"] = line[2:].strip()
                        break
            
            # Generate embedding
            embedding = self.embedding_model.encode(content).tolist()
            
            # Create unique ID
            doc_id = str(uuid.uuid4())
            
            # Store in ChromaDB
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                embeddings=[embedding],
                ids=[doc_id]
            )
            
            logger.info(f"✅ Stored: {relative_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error processing {file_path}: {e}")
            return False
    
    def update_knowledge_base(self):
        """Update the knowledge base with all documentation."""
        logger.info("🚀 Starting direct knowledge base update...")
        
        # Get all documentation files
        doc_files = self.get_documentation_files()
        logger.info(f"📚 Found {len(doc_files)} documentation files to index")
        
        # Process files
        successful = 0
        failed = 0
        
        for file_path in doc_files:
            if self.store_document(file_path):
                successful += 1
            else:
                failed += 1
        
        logger.info(f"📊 Knowledge base update complete!")
        logger.info(f"   ✅ Successfully indexed: {successful} documents")
        logger.info(f"   ❌ Failed: {failed} documents")
        
        return successful > 0
    
    def verify_indexing(self):
        """Verify that documents were properly indexed."""
        logger.info("🔍 Verifying knowledge base indexing...")
        
        # Get collection stats
        count = self.collection.count()
        logger.info(f"📊 Total documents in collection: {count}")
        
        # Test queries
        test_queries = [
            "quick start guide setup",
            "agent configuration", 
            "claude commands",
            "development workflow",
            "project structure"
        ]
        
        for query in test_queries:
            try:
                # Generate query embedding
                query_embedding = self.embedding_model.encode(query).tolist()
                
                # Query the collection
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=3
                )
                
                logger.info(f"Query '{query}': Found {len(results['documents'][0])} results")
                
                # Show top results
                for i, (doc, metadata) in enumerate(zip(results['documents'][0][:2], results['metadatas'][0][:2])):
                    file_path = metadata.get('file_path', 'unknown')
                    doc_type = metadata.get('doc_type', 'unknown')
                    logger.info(f"  - {file_path} ({doc_type})")
                    
            except Exception as e:
                logger.error(f"Error querying '{query}': {e}")

def main():
    """Main function to update knowledge base."""
    updater = DirectKnowledgeUpdater()
    
    try:
        success = updater.update_knowledge_base()
        if success:
            updater.verify_indexing()
            logger.info("🎉 Knowledge base update completed successfully!")
        else:
            logger.error("❌ Knowledge base update failed!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Knowledge base update failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
