#!/usr/bin/env python3
"""Simple initialization test for the Agent Factory project."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test that core imports work."""
    try:
        from config.settings import settings
        print(f"✅ Configuration loaded: {settings.environment} environment")
        
        from config.logging import get_logger
        logger = get_logger(__name__)
        logger.info("Testing logging", test_id="init")
        print("✅ Logging configured")
        
        from agent_factory.models import AgentMessage, TaskSpecification
        
        message = AgentMessage(sender_id="test", recipient_id="test")
        task = TaskSpecification(title="Test Task")
        
        print("✅ Data models working")
        print("✅ Project foundation setup complete!")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
