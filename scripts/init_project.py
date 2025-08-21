#!/usr/bin/env python3
"""Initialize the Agent Factory project.

This script validates that all components are properly configured and working.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config.logging import get_logger
from config.settings import settings

console = Console()
logger = get_logger(__name__)


async def check_dependencies() -> bool:
    """Check if all required dependencies are available."""
    dependencies = [
        ("langchain", "LangChain agent framework"),
        ("chromadb", "ChromaDB vector database"),
        ("redis", "Redis client"),
        ("fastapi", "FastAPI web framework"),
        ("pydantic", "Pydantic data validation"),
        ("structlog", "Structured logging"),
    ]
    
    table = Table(title="Dependency Check")
    table.add_column("Package", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Status", justify="center")
    
    all_good = True
    
    for package, description in dependencies:
        try:
            __import__(package)
            table.add_row(package, description, "✅ Available")
        except ImportError:
            table.add_row(package, description, "❌ Missing")
            all_good = False
    
    console.print(table)
    return all_good


def check_configuration() -> bool:
    """Check if configuration is properly loaded."""
    console.print("\n[bold blue]Configuration Check[/bold blue]")
    
    try:
        config_items = [
            ("Environment", settings.environment),
            ("Debug Mode", settings.debug),
            ("Data Directory", settings.data_directory),
            ("Redis Host", settings.redis.host),
            ("Redis Port", settings.redis.port),
            ("Chroma Directory", settings.chroma.persist_directory),
            ("API Port", settings.api.port),
        ]
        
        for name, value in config_items:
            console.print(f"  {name}: [green]{value}[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]Configuration error: {e}[/red]")
        return False


def check_directories() -> bool:
    """Check if required directories exist or can be created."""
    console.print("\n[bold blue]Directory Structure Check[/bold blue]")
    
    required_dirs = [
        settings.data_directory,
        settings.logs_directory,
        settings.chroma.persist_directory,
        "src/agents",
        "src/knowledge",
        "src/communication",
        "src/workflows",
        "src/api",
        "src/tools",
        "src/config",
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            console.print(f"  {dir_path}: [green]✅ Exists[/green]")
        else:
            try:
                path.mkdir(parents=True, exist_ok=True)
                console.print(f"  {dir_path}: [yellow]📁 Created[/yellow]")
            except Exception as e:
                console.print(f"  {dir_path}: [red]❌ Failed - {e}[/red]")
                all_good = False
    
    return all_good


async def test_basic_functionality() -> bool:
    """Test basic functionality of core components."""
    console.print("\n[bold blue]Basic Functionality Test[/bold blue]")
    
    try:
        # Test logging
        logger.info("Testing logging functionality", test_id="init_project")
        console.print("  Logging: [green]✅ Working[/green]")
        
        # Test data models
        from agent_factory.models import AgentMessage, TaskSpecification
        
        message = AgentMessage(
            sender_id="test_sender",
            recipient_id="test_recipient",
            payload={"test": "data"}
        )
        
        task = TaskSpecification(
            title="Test Task",
            description="Test task description"
        )
        
        console.print("  Data Models: [green]✅ Working[/green]")
        
        # Test serialization
        message_dict = message.to_dict()
        task_dict = task.to_dict()
        
        console.print("  Serialization: [green]✅ Working[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"  [red]❌ Basic functionality test failed: {e}[/red]")
        return False


def main():
    """Main entry point."""
    import sys
    
    quiet = "--quiet" in sys.argv or "-q" in sys.argv
    asyncio.run(main_async(quiet))


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    asyncio.run(main())
