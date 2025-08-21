"""ChromaDB vector store implementation for knowledge storage."""

import asyncio
import logging
from typing import Any

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from ...models import KnowledgeEntry, SourceType

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """Vector store implementation using ChromaDB."""

    def __init__(
        self,
        persist_directory: str = "./data/chroma",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        collection_name: str = "agent_knowledge",
    ):
        """Initialize the ChromaDB vector store.

        Args:
            persist_directory: Directory to persist the database
            embedding_model: Sentence transformer model for embeddings
            collection_name: Name of the collection to use
        """
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model
        self.collection_name = collection_name

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"description": "Agent knowledge base"}
        )

        logger.info(f"Initialized ChromaDB with collection: {collection_name}")

    async def embed_text(self, text: str) -> list[float]:
        """Generate embeddings for text asynchronously.

        Args:
            text: Text to embed

        Returns:
            List of float values representing the embedding
        """
        # Run embedding generation in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(None, self.embedding_model.encode, text)
        return embedding.tolist()

    async def store_knowledge(self, entry: KnowledgeEntry) -> str:
        """Store a knowledge entry in the vector store.

        Args:
            entry: Knowledge entry to store

        Returns:
            ID of the stored entry
        """
        try:
            # Generate embedding if not provided
            if not entry.embedding:
                entry.embedding = await self.embed_text(entry.content)

            # Prepare metadata
            metadata = {
                "source_type": entry.source_type.value,
                "created_at": entry.created_at.isoformat(),
                "tags": ",".join(entry.tags),
                **entry.metadata,
            }

            # Store in ChromaDB
            self.collection.add(
                ids=[entry.id],
                embeddings=[entry.embedding],
                documents=[entry.content],
                metadatas=[metadata],
            )

            logger.debug(f"Stored knowledge entry: {entry.id}")
            return entry.id

        except Exception as e:
            logger.error(f"Failed to store knowledge entry: {e}")
            raise

    async def query_similar(
        self,
        query: str,
        n_results: int = 5,
        source_type: SourceType | None = None,
        tags: list[str] | None = None,
    ) -> list[KnowledgeEntry]:
        """Query for similar knowledge entries.

        Args:
            query: Text query to search for
            n_results: Number of results to return
            source_type: Filter by source type
            tags: Filter by tags

        Returns:
            List of knowledge entries sorted by similarity
        """
        try:
            # Generate query embedding
            query_embedding = await self.embed_text(query)

            # Build where clause for filtering
            where_clause = {}
            if source_type:
                where_clause["source_type"] = source_type.value

            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause if where_clause else None,
            )

            # Convert results to KnowledgeEntry objects
            entries = []
            for i in range(len(results["ids"][0])):
                metadata = results["metadatas"][0][i]

                # Filter by tags if specified
                entry_tags = (
                    metadata.get("tags", "").split(",") if metadata.get("tags") else []
                )
                if tags and not any(tag in entry_tags for tag in tags):
                    continue

                # Reconstruct metadata dict
                clean_metadata = {
                    k: v
                    for k, v in metadata.items()
                    if k not in ["source_type", "created_at", "tags"]
                }

                entry = KnowledgeEntry(
                    id=results["ids"][0][i],
                    content=results["documents"][0][i],
                    embedding=[],  # Don't return embeddings for efficiency
                    metadata=clean_metadata,
                    source_type=SourceType(metadata["source_type"]),
                    tags=entry_tags,
                )
                entries.append(entry)

            logger.debug(f"Found {len(entries)} similar entries for query")
            return entries

        except Exception as e:
            logger.error(f"Failed to query similar entries: {e}")
            raise

    async def get_relevant_context(
        self, query: str, limit: int = 5, source_types: list[SourceType] | None = None
    ) -> list[str]:
        """Get relevant context for a query.

        Args:
            query: Query to search for context
            limit: Maximum number of context items
            source_types: Filter by specific source types

        Returns:
            List of relevant context strings
        """
        try:
            context_items = []

            if source_types:
                # Query each source type separately
                for source_type in source_types:
                    entries = await self.query_similar(
                        query,
                        n_results=limit // len(source_types),
                        source_type=source_type,
                    )
                    context_items.extend([entry.content for entry in entries])
            else:
                # Query all types
                entries = await self.query_similar(query, n_results=limit)
                context_items = [entry.content for entry in entries]

            return context_items[:limit]

        except Exception as e:
            logger.error(f"Failed to get relevant context: {e}")
            return []

    async def store_pattern(self, pattern: dict[str, Any]) -> str:
        """Store a success pattern in the knowledge base.

        Args:
            pattern: Pattern data to store

        Returns:
            ID of the stored pattern
        """
        entry = KnowledgeEntry(
            content=f"Success Pattern: {pattern.get('description', '')}",
            metadata=pattern,
            source_type=SourceType.PATTERN,
            tags=["success", "pattern"],
        )
        return await self.store_knowledge(entry)

    async def store_failure_pattern(self, failure: dict[str, Any]) -> str:
        """Store a failure pattern for learning.

        Args:
            failure: Failure analysis data

        Returns:
            ID of the stored failure pattern
        """
        entry = KnowledgeEntry(
            content=f"Failure Pattern: {failure.get('description', '')}",
            metadata=failure,
            source_type=SourceType.FAILURE,
            tags=["failure", "learning"],
        )
        return await self.store_knowledge(entry)

    async def store_outcome(self, prp: Any, response: Any) -> str:
        """Store execution outcome for learning.

        Args:
            prp: The PRP that was executed
            response: The agent response

        Returns:
            ID of the stored outcome
        """
        outcome_type = SourceType.SUCCESS if response.success else SourceType.FAILURE

        entry = KnowledgeEntry(
            content=f"Execution Outcome: {prp.goal}",
            metadata={
                "prp_goal": prp.goal,
                "success": response.success,
                "execution_time": response.execution_time,
                "agent_id": response.agent_id,
            },
            source_type=outcome_type,
            tags=["outcome", "execution"],
        )
        return await self.store_knowledge(entry)

    async def get_stats(self) -> dict[str, Any]:
        """Get statistics about the knowledge base.

        Returns:
            Dictionary containing knowledge base statistics
        """
        try:
            count = self.collection.count()

            # Get counts by source type
            type_counts = {}
            for source_type in SourceType:
                results = self.collection.query(
                    query_texts=[""],
                    n_results=1,
                    where={"source_type": source_type.value},
                )
                type_counts[source_type.value] = len(results.get("ids", []))

            return {
                "total_entries": count,
                "by_source_type": type_counts,
                "collection_name": self.collection_name,
            }

        except Exception as e:
            logger.error(f"Failed to get knowledge base stats: {e}")
            return {}

    async def delete_entry(self, entry_id: str) -> bool:
        """Delete a knowledge entry.

        Args:
            entry_id: ID of the entry to delete

        Returns:
            True if deletion was successful
        """
        try:
            self.collection.delete(ids=[entry_id])
            logger.debug(f"Deleted knowledge entry: {entry_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete entry {entry_id}: {e}")
            return False

    async def reset_collection(self) -> bool:
        """Reset the entire collection.

        Returns:
            True if reset was successful
        """
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Agent knowledge base"},
            )
            logger.info(f"Reset collection: {self.collection_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")
            return False
