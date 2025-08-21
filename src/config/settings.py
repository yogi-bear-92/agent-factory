"""Configuration settings for the Agent Factory framework."""

from __future__ import annotations

import os
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    """Redis configuration."""

    host: str = Field(default="localhost", description="Redis server host")
    port: int = Field(default=6379, description="Redis server port")
    db: int = Field(default=0, description="Redis database number")
    password: str | None = Field(default=None, description="Redis password")
    decode_responses: bool = Field(default=True, description="Decode Redis responses")
    max_connections: int = Field(default=10, description="Max connection pool size")

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class ChromaSettings(BaseSettings):
    """ChromaDB configuration."""

    persist_directory: str = Field(
        default="./data/chroma", description="Directory to persist ChromaDB data"
    )
    collection_name: str = Field(
        default="agent_knowledge", description="Default collection name"
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2", description="Sentence transformer model name"
    )
    chunk_size: int = Field(default=1000, description="Text chunk size for embeddings")
    chunk_overlap: int = Field(default=200, description="Overlap between text chunks")

    model_config = SettingsConfigDict(env_prefix="CHROMA_")


class APISettings(BaseSettings):
    """API configuration."""

    host: str = Field(default="0.0.0.0", description="API server host")
    port: int = Field(default=8000, description="API server port")
    workers: int = Field(default=1, description="Number of worker processes")
    api_key: str = Field(default="dev-key", description="API authentication key")
    cors_origins: list[str] = Field(default=["*"], description="CORS allowed origins")
    request_timeout: int = Field(default=300, description="Request timeout in seconds")

    model_config = SettingsConfigDict(env_prefix="API_")


class LLMSettings(BaseSettings):
    """Language model configuration."""

    provider: str = Field(default="openai", description="LLM provider")
    model: str = Field(default="gpt-3.5-turbo", description="Model name")
    api_key: str = Field(default="", description="API key for LLM provider")
    base_url: str | None = Field(default=None, description="Custom base URL")
    max_tokens: int = Field(default=2000, description="Maximum tokens per request")
    temperature: float = Field(default=0.1, description="Model temperature")

    model_config = SettingsConfigDict(env_prefix="LLM_")


class AgentSettings(BaseSettings):
    """Agent system configuration."""

    max_concurrent_agents: int = Field(
        default=5, description="Maximum concurrent agents"
    )
    task_timeout: int = Field(default=3600, description="Task timeout in seconds")
    heartbeat_interval: int = Field(
        default=30, description="Agent heartbeat interval in seconds"
    )
    max_retries: int = Field(default=3, description="Maximum task retries")
    backoff_factor: float = Field(default=2.0, description="Retry backoff factor")

    model_config = SettingsConfigDict(env_prefix="AGENT_")


class MonitoringSettings(BaseSettings):
    """Monitoring and observability configuration."""

    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=9090, description="Metrics server port")
    log_level: str = Field(default="INFO", description="Logging level")
    enable_tracing: bool = Field(
        default=False, description="Enable OpenTelemetry tracing"
    )
    jaeger_endpoint: str | None = Field(
        default=None, description="Jaeger collector endpoint"
    )

    model_config = SettingsConfigDict(env_prefix="MONITORING_")


class AzureOpenAISettings(BaseSettings):
    """Azure AI Foundry (Azure OpenAI) configuration."""

    endpoint: str = Field(default="", description="Azure OpenAI endpoint URL")
    api_key: str = Field(default="", description="Azure OpenAI API key")
    deployment: str = Field(default="", description="Azure OpenAI deployment name")
    api_version: str = Field(
        default="2024-05-01-preview", description="Azure OpenAI API version"
    )
    use_aad: bool = Field(
        default=False,
        description="Use AAD authentication (requires environment setup)",
    )

    model_config = SettingsConfigDict(env_prefix="AZURE_OPENAI_")


class Settings(BaseSettings):
    """Main application settings."""

    # Environment
    environment: str = Field(
        default="development", description="Application environment"
    )
    debug: bool = Field(default=True, description="Debug mode")

    # Component settings
    redis: RedisSettings = Field(default_factory=RedisSettings)
    chroma: ChromaSettings = Field(default_factory=ChromaSettings)
    api: APISettings = Field(default_factory=APISettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    agents: AgentSettings = Field(default_factory=AgentSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    azure_openai: AzureOpenAISettings = Field(default_factory=AzureOpenAISettings)

    # Paths
    data_directory: str = Field(default="./data", description="Data storage directory")
    logs_directory: str = Field(default="./logs", description="Logs directory")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # Create necessary directories
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(self.logs_directory, exist_ok=True)
        os.makedirs(self.chroma.persist_directory, exist_ok=True)


# Global settings instance
settings = Settings()
