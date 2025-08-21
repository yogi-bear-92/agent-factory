"""Tests for ChromaVectorStore implementation."""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.agent_factory.models import KnowledgeEntry, SourceType
from src.knowledge.vector_store.chroma_client import ChromaVectorStore


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def chroma_store(temp_dir):
    """Create ChromaVectorStore instance for testing."""
    return ChromaVectorStore(
        persist_directory=str(Path(temp_dir) / "test_chroma"),
        collection_name="test_collection"
    )


@pytest.mark.asyncio
async def test_store_and_query_basic(chroma_store):
    """Test basic store and query functionality."""
    # Create test knowledge entry
    entry = KnowledgeEntry(
        content="This is a test knowledge entry about Python programming.",
        source_type=SourceType.DOCUMENTATION,
        tags=["python", "programming", "test"]
    )
    
    # Store the entry
    stored_id = await chroma_store.store_knowledge(entry)
    assert stored_id == entry.id
    
    # Query for similar content
    results = await chroma_store.query_similar("Python programming", n_results=5)
    assert len(results) >= 1
    assert any(entry.id == result.id for result in results)


@pytest.mark.asyncio
async def test_get_relevant_context(chroma_store):
    """Test context retrieval."""
    # Store multiple entries
    entries = [
        KnowledgeEntry(
            content="Python is a programming language",
            source_type=SourceType.DOCUMENTATION,
            tags=["python"]
        ),
        KnowledgeEntry(
            content="JavaScript is used for web development",
            source_type=SourceType.DOCUMENTATION, 
            tags=["javascript"]
        )
    ]
    
    for entry in entries:
        await chroma_store.store_knowledge(entry)
    
    # Get relevant context
    context = await chroma_store.get_relevant_context("programming language")
    assert len(context) > 0
    assert any("Python" in item for item in context)


if __name__ == "__main__":
    pytest.main([__file__])
