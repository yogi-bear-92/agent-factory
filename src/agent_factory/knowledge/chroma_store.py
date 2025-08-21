"""Chroma vector database implementation for knowledge storage."""

import logging
from typing import Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from ..models import KnowledgeEntry, SourceType

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """Vector store implementation using Chroma database."""

    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        collection_name: str = "agent_knowledge",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        """Initialize Chroma vector store.

        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
            embedding_model: Model for generating embeddings
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model

        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Agent Factory knowledge base"},
        )

        logger.info(f"Initialized Chroma vector store at {persist_directory}")

    async def store_entry(self, entry: KnowledgeEntry) -> str:
        """Store a knowledge entry in the vector database.

        Args:
            entry: Knowledge entry to store

        Returns:
            ID of the stored entry
        """
        # Generate embedding if not provided
        if not entry.embedding:
            entry.embedding = self._generate_embedding(entry.content)

        # Prepare metadata
        metadata = {
            "source_type": entry.source_type.value,
            "created_at": entry.created_at.isoformat(),
            "tags": ",".join(entry.tags) if entry.tags else "",
            **entry.metadata,
        }

        # Store in Chroma
        self.collection.add(
            ids=[entry.id],
            embeddings=[entry.embedding],
            documents=[entry.content],
            metadatas=[metadata],
        )

        logger.debug(f"Stored knowledge entry {entry.id}")
        return entry.id

    async def store_multiple(self, entries: list[KnowledgeEntry]) -> list[str]:
        """Store multiple knowledge entries efficiently.

        Args:
            entries: List of knowledge entries to store

        Returns:
            List of IDs of stored entries
        """
        if not entries:
            return []

        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for entry in entries:
            # Generate embedding if not provided
            if not entry.embedding:
                entry.embedding = self._generate_embedding(entry.content)

            # Prepare metadata
            metadata = {
                "source_type": entry.source_type.value,
                "created_at": entry.created_at.isoformat(),
                "tags": ",".join(entry.tags) if entry.tags else "",
                **entry.metadata,
            }

            ids.append(entry.id)
            embeddings.append(entry.embedding)
            documents.append(entry.content)
            metadatas.append(metadata)

        # Store all entries in batch
        self.collection.add(
            ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
        )

        logger.info(f"Stored {len(entries)} knowledge entries")
        return ids

    async def query_similar(
        self,
        query: str,
        n_results: int = 5,
        source_type: SourceType | None = None,
        tags: list[str] | None = None,
    ) -> list[KnowledgeEntry]:
        """Query for similar knowledge entries.

        Args:
            query: Query string
            n_results: Number of results to return
            source_type: Filter by source type
            tags: Filter by tags

        Returns:
            List of similar knowledge entries
        """
        # Generate query embedding
        query_embedding = self._generate_embedding(query)

        # Build where clause for filtering
        where_clause = {}
        if source_type:
            where_clause["source_type"] = source_type.value

        # Query Chroma
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_clause if where_clause else None,
        )

        # Convert results to KnowledgeEntry objects
        entries = []
        if results["ids"] and results["ids"][0]:
            for i, entry_id in enumerate(results["ids"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                document = results["documents"][0][i] if results["documents"] else ""

                # Parse tags
                tags_str = metadata.get("tags", "")
                entry_tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

                # Create KnowledgeEntry
                entry = KnowledgeEntry(
                    id=entry_id,
                    content=document,
                    source_type=SourceType(
                        metadata.get("source_type", "documentation")
                    ),
                    tags=entry_tags,
                    metadata={
                        k: v
                        for k, v in metadata.items()
                        if k not in ["source_type", "created_at", "tags"]
                    },
                )
                entries.append(entry)

        logger.debug(f"Found {len(entries)} similar entries for query: {query[:50]}...")
        return entries

    async def get_entry(self, entry_id: str) -> KnowledgeEntry | None:
        """Get a specific knowledge entry by ID.

        Args:
            entry_id: ID of the entry to retrieve

        Returns:
            Knowledge entry if found, None otherwise
        """
        results = self.collection.get(ids=[entry_id])

        if not results["ids"] or not results["ids"][0]:
            return None

        metadata = results["metadatas"][0] if results["metadatas"] else {}
        document = results["documents"][0] if results["documents"] else ""

        # Parse tags
        tags_str = metadata.get("tags", "")
        entry_tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

        return KnowledgeEntry(
            id=entry_id,
            content=document,
            source_type=SourceType(metadata.get("source_type", "documentation")),
            tags=entry_tags,
            metadata={
                k: v
                for k, v in metadata.items()
                if k not in ["source_type", "created_at", "tags"]
            },
        )

    async def delete_entry(self, entry_id: str) -> bool:
        """Delete a knowledge entry.

        Args:
            entry_id: ID of the entry to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            self.collection.delete(ids=[entry_id])
            logger.debug(f"Deleted knowledge entry {entry_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete entry {entry_id}: {e}")
            return False

    async def get_context_for_query(
        self,
        query: str,
        max_context_length: int = 2000,
        source_types: list[SourceType] | None = None,
    ) -> str:
        """Get formatted context for a query using RAG.

        Args:
            query: Query to get context for
            max_context_length: Maximum length of context
            source_types: Types of sources to include

        Returns:
            Formatted context string
        """
        context_parts = []
        current_length = 0

        # Query for relevant entries
        if source_types:
            all_entries = []
            for source_type in source_types:
                entries = await self.query_similar(
                    query, n_results=3, source_type=source_type
                )
                all_entries.extend(entries)
        else:
            all_entries = await self.query_similar(query, n_results=10)

        # Build context string
        for entry in all_entries:
            entry_text = (
                f"\n--- {entry.source_type.value.upper()} ---\n{entry.content}\n"
            )
            if current_length + len(entry_text) > max_context_length:
                break
            context_parts.append(entry_text)
            current_length += len(entry_text)

        return "".join(context_parts)

    def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        embedding = self.embedding_model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    async def get_stats(self) -> dict[str, Any]:
        """Get database statistics.

        Returns:
            Dictionary with database statistics
        """
        count = self.collection.count()

        # Get source type distribution
        all_results = self.collection.get()
        source_types = {}
        if all_results["metadatas"]:
            for metadata in all_results["metadatas"]:
                source_type = metadata.get("source_type", "unknown")
                source_types[source_type] = source_types.get(source_type, 0) + 1

        return {
            "total_entries": count,
            "source_type_distribution": source_types,
            "collection_name": self.collection_name,
            "embedding_model": self.embedding_model_name,
        }

    async def clear_all(self) -> None:
        """Clear all entries from the database."""
        # Get all IDs and delete them
        all_results = self.collection.get()
        if all_results["ids"]:
            self.collection.delete(ids=all_results["ids"])
        logger.info("Cleared all entries from knowledge base")
