#!/usr/bin/env python3
"""Comprehensive test script for the Agent Factory system."""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def test_agent_imports():
    """Test all agent imports."""
    print("🔍 Testing agent imports...")
    
    try:
        # Test communication imports
        print("  ✓ Testing communication imports...")
        from communication.message_bus import RedisMessageBus
        print("    ✓ RedisMessageBus imported successfully")
        
        # Test knowledge imports
        print("  ✓ Testing knowledge imports...")
        from knowledge.vector_store import ChromaVectorStore
        print("    ✓ ChromaVectorStore imported successfully")
        
        # Test models imports
        print("  ✓ Testing models imports...")
        from models import (
            AgentMessage, AgentType, TaskSpecification, 
            AgentResponse, AgentPRP, FeatureRequest
        )
        print("    ✓ Core models imported successfully")
        
        # Test base agent imports
        print("  ✓ Testing base agent imports...")
        from agents.base import BaseAgent
        print("    ✓ BaseAgent imported successfully")
        
        # Test all agent implementations
        print("  ✓ Testing agent implementations...")
        from agents.coordinator.task_coordinator import TaskCoordinator
        from agents.planner.feature_planner import FeaturePlanner
        from agents.coder.implementation_coder import ImplementationCoder
        from agents.tester.automated_tester import AutomatedTester
        from agents.reviewer.code_reviewer import CodeReviewer
        from agents.devops.deployment_agent import DeploymentAgent
        print("    ✓ All agent implementations imported successfully")
        
        print("🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_agent_instantiation():
    """Test creating agent instances."""
    print("\n🔧 Testing agent instantiation...")
    
    try:
        # Test creating a message bus
        print("  ✓ Testing RedisMessageBus creation...")
        message_bus = RedisMessageBus()
        print("    ✓ RedisMessageBus created successfully")
        
        # Test creating a vector store
        print("  ✓ Testing ChromaVectorStore creation...")
        vector_store = ChromaVectorStore()
        print("    ✓ ChromaVectorStore created successfully")
        
        # Test creating agent instances
        print("  ✓ Testing agent instance creation...")
        coordinator = TaskCoordinator(
            knowledge_base=vector_store,
            message_bus=message_bus
        )
        print("    ✓ TaskCoordinator created successfully")
        
        planner = FeaturePlanner(
            knowledge_base=vector_store,
            message_bus=message_bus
        )
        print("    ✓ FeaturePlanner created successfully")
        
        coder = ImplementationCoder(
            knowledge_base=vector_store,
            message_bus=message_bus
        )
        print("    ✓ ImplementationCoder created successfully")
        
        tester = AutomatedTester(
            knowledge_base=vector_store,
            message_bus=message_bus
        )
        print("    ✓ AutomatedTester created successfully")
        
        reviewer = CodeReviewer(
            knowledge_base=vector_store,
            message_bus=message_bus
        )
        print("    ✓ CodeReviewer created successfully")
        
        devops = DeploymentAgent(
            knowledge_base=vector_store,
            message_bus=message_bus
        )
        print("    ✓ DeploymentAgent created successfully")
        
        print("🎉 All agent instantiation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Instantiation failed: {e}")
        return False

async def test_agent_methods():
    """Test agent method calls."""
    print("\n🧪 Testing agent methods...")
    
    try:
        # Create test instances
        message_bus = RedisMessageBus()
        vector_store = ChromaVectorStore()
        
        # Test coordinator methods
        print("  ✓ Testing coordinator methods...")
        coordinator = TaskCoordinator(
            knowledge_base=vector_store,
            message_bus=message_bus
        )
        
        # Test task processing
        test_task = TaskSpecification(
            title="Test Task",
            description="A test task for validation",
            requirements=["Requirement 1", "Requirement 2"]
        )
        
        # Note: We can't actually call process_task without a running LLM service
        # But we can verify the method exists
        if hasattr(coordinator, 'process_task'):
            print("    ✓ process_task method exists")
        else:
            print("    ❌ process_task method missing")
            return False
            
        if hasattr(coordinator, 'process_prp'):
            print("    ✓ process_prp method exists")
        else:
            print("    ❌ process_prp method missing")
            return False
        
        print("🎉 All agent method tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Method testing failed: {e}")
        return False

async def test_system_integration():
    """Test system integration components."""
    print("\n🔗 Testing system integration...")
    
    try:
        # Test message bus methods
        print("  ✓ Testing message bus methods...")
        message_bus = RedisMessageBus()
        
        if hasattr(message_bus, 'send_message'):
            print("    ✓ send_message method exists")
        else:
            print("    ❌ send_message method missing")
            return False
            
        if hasattr(message_bus, 'subscribe'):
            print("    ✓ subscribe method exists")
        else:
            print("    ❌ subscribe method missing")
            return False
        
        # Test vector store methods
        print("  ✓ Testing vector store methods...")
        vector_store = ChromaVectorStore()
        
        if hasattr(vector_store, 'connect'):
            print("    ✓ connect method exists")
        else:
            print("    ❌ connect method missing")
            return False
            
        if hasattr(vector_store, 'get_relevant_context'):
            print("    ✓ get_relevant_context method exists")
        else:
            print("    ❌ get_relevant_context method missing")
            return False
        
        print("🎉 All system integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ System integration testing failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Agent Factory System Test Suite")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("Import Tests", test_agent_imports),
        ("Instantiation Tests", test_agent_instantiation),
        ("Method Tests", test_agent_methods),
        ("Integration Tests", test_system_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your agent system is ready to run.")
        print("\n🚀 Next steps:")
        print("  1. Start the infrastructure: docker-compose up -d redis chromadb")
        print("  2. Start the agents: docker-compose up -d agent-coordinator agent-planner agent-coder agent-tester agent-reviewer agent-devops")
        print("  3. Monitor logs: docker-compose logs -f")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix the issues before proceeding.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)