"""Communication layer for agent coordination."""

from .redis_messenger import RedisMessageBus

__all__ = ["RedisMessageBus"]
