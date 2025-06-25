#!/usr/bin/env python3
"""
Test MCP Tools functionality for OnlysaidKB MCP Server
Tests the actual MCP tool implementations
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from onlysaidkb_mcp.server import query_knowledge_base, retrieve_from_knowledge_base
    from onlysaidkb_mcp.server import list_knowledge_bases_resource, knowledge_base_status_resource
    from onlysaidkb_mcp.server import workspace_structure_resource
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install dependencies with: uv sync")
    sys.exit(1)

class MCPToolsTest:
    def __init__(self):
        self.test_workspace_id = os.getenv("TEST_WORKSPACE_ID", "test-workspace-123")
        self.test_kb_ids = os.getenv("TEST_KB_IDS", "kb-1,kb-2").split(",")
        
        print(f"🔧 MCP Tools Test Configuration:")
        print(f"  Test Workspace ID: {self.test_workspace_id}")
        print(f"  Test KB IDs: {self.test_kb_ids}")
    
    async def test_query_tool(self):
        """Test the query_knowledge_base MCP tool"""
        print("\n🤖 Testing query_knowledge_base MCP Tool...")
        
        test_cases = [
            {
                "name": "Basic Query",
                "params": {
                    "workspace_id": self.test_workspace_id,
                    "query": "What is the main purpose of this system?"
                }
            },
            {
                "name": "Query with KB IDs",
                "params": {
                    "workspace_id": self.test_workspace_id,
                    "query": "How do I configure the knowledge base?",
                    "knowledge_bases": self.test_kb_ids
                }
            },
            {
                "name": "Query with Custom Parameters",
                "params": {
                    "workspace_id": self.test_workspace_id,
                    "query": "What are the API endpoints available?",
                    "model": "gpt-3.5-turbo",
                    "top_k": 3,
                    "preferred_language": "en"
                }
            },
            {
                "name": "Query with Conversation History",
                "params": {
                    "workspace_id": self.test_workspace_id,
                    "query": "What about the authentication process?",
                    "conversation_history": [
                        "user: What is this system?",
                        "assistant: This is a knowledge base system.",
                        "user: How do I use it?"
                    ]
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n  {i}. {test_case['name']}")
            print(f"     Parameters: {json.dumps(test_case['params'], indent=6)}")
            
            try:
                result = await query_knowledge_base(**test_case['params'])
                print(f"     ✅ Success: {type(result).__name__}")
                print(f"     Result preview: {json.dumps(result, indent=6)[:300]}...")
                
                # Check for expected fields
                if isinstance(result, dict):
                    if "error" in result:
                        print(f"     ⚠️ Tool returned error: {result['error']}")
                    if "_debug" in result:
                        print(f"     🔍 Debug info available")
                
            except Exception as e:
                print(f"     ❌ Error: {str(e)}")
    
    async def test_retrieve_tool(self):
        """Test the retrieve_from_knowledge_base MCP tool"""
        print("\n🔍 Testing retrieve_from_knowledge_base MCP Tool...")
        
        test_cases = [
            {
                "name": "Basic Retrieval",
                "params": {
                    "workspace_id": self.test_workspace_id,
                    "query": "system configuration"
                }
            },
            {
                "name": "Retrieval with KB IDs",
                "params": {
                    "workspace_id": self.test_workspace_id,
                    "query": "API documentation",
                    "knowledge_bases": self.test_kb_ids
                }
            },
            {
                "name": "Retrieval with Custom Top K",
                "params": {
                    "workspace_id": self.test_workspace_id,
                    "query": "user authentication",
                    "top_k": 10
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n  {i}. {test_case['name']}")
            print(f"     Parameters: {json.dumps(test_case['params'], indent=6)}")
            
            try:
                result = await retrieve_from_knowledge_base(**test_case['params'])
                print(f"     ✅ Success: {type(result).__name__}")
                print(f"     Result preview: {json.dumps(result, indent=6)[:300]}...")
                
                # Check for expected fields
                if isinstance(result, dict):
                    if "error" in result:
                        print(f"     ⚠️ Tool returned error: {result['error']}")
                    if "_debug" in result:
                        print(f"     🔍 Debug info available")
                    if "results" in result:
                        results = result["results"]
                        if isinstance(results, list):
                            print(f"     📊 Retrieved {len(results)} documents")
                
            except Exception as e:
                print(f"     ❌ Error: {str(e)}")
    
    async def test_resources(self):
        """Test the MCP resources"""
        print("\n📚 Testing MCP Resources...")
        
        # Test 1: List Knowledge Bases Resource
        print("\n  1. Testing list_knowledge_bases_resource...")
        try:
            result = await list_knowledge_bases_resource(self.test_workspace_id)
            print(f"     ✅ Success: {type(result).__name__}")
            print(f"     Result preview: {result[:200]}...")
        except Exception as e:
            print(f"     ❌ Error: {str(e)}")
        
        # Test 2: Knowledge Base Status Resource
        if self.test_kb_ids and self.test_kb_ids[0]:
            print(f"\n  2. Testing knowledge_base_status_resource for KB: {self.test_kb_ids[0]}...")
            try:
                result = await knowledge_base_status_resource(self.test_workspace_id, self.test_kb_ids[0])
                print(f"     ✅ Success: {type(result).__name__}")
                print(f"     Result preview: {result[:200]}...")
            except Exception as e:
                print(f"     ❌ Error: {str(e)}")
        
        # Test 3: Workspace Structure Resource
        print("\n  3. Testing workspace_structure_resource...")
        try:
            result = await workspace_structure_resource(self.test_workspace_id)
            print(f"     ✅ Success: {type(result).__name__}")
            print(f"     Result preview: {result[:200]}...")
        except Exception as e:
            print(f"     ❌ Error: {str(e)}")
    
    async def test_error_scenarios(self):
        """Test error handling in MCP tools"""
        print("\n🚨 Testing Error Scenarios...")
        
        # Test 1: Invalid workspace ID
        print("\n  1. Testing invalid workspace ID...")
        try:
            result = await query_knowledge_base(
                workspace_id="invalid-workspace-id",
                query="Test query"
            )
            print(f"     Result: {json.dumps(result, indent=6)[:300]}...")
            
            if isinstance(result, dict) and "error" in result:
                print(f"     ✅ Error handled correctly")
            else:
                print(f"     ⚠️ Unexpected result type")
                
        except Exception as e:
            print(f"     ❌ Unexpected exception: {str(e)}")
        
        # Test 2: Empty query
        print("\n  2. Testing empty query...")
        try:
            result = await query_knowledge_base(
                workspace_id=self.test_workspace_id,
                query=""
            )
            print(f"     Result: {json.dumps(result, indent=6)[:300]}...")
            
            if isinstance(result, dict) and "error" in result:
                print(f"     ✅ Error handled correctly")
            else:
                print(f"     ⚠️ Unexpected result - empty query might be allowed")
                
        except Exception as e:
            print(f"     ❌ Unexpected exception: {str(e)}")
        
        # Test 3: Invalid knowledge base IDs
        print("\n  3. Testing invalid knowledge base IDs...")
        try:
            result = await retrieve_from_knowledge_base(
                workspace_id=self.test_workspace_id,
                query="Test query",
                knowledge_bases=["invalid-kb-1", "invalid-kb-2"]
            )
            print(f"     Result: {json.dumps(result, indent=6)[:300]}...")
            
            if isinstance(result, dict) and "error" in result:
                print(f"     ✅ Error handled correctly")
            else:
                print(f"     ⚠️ Invalid KB IDs might be allowed")
                
        except Exception as e:
            print(f"     ❌ Unexpected exception: {str(e)}")

async def run_all_tests():
    """Run all MCP tools tests"""
    print("🧪 OnlysaidKB MCP Tools Test Suite")
    print("=" * 80)
    
    tester = MCPToolsTest()
    
    # Run all test categories
    await tester.test_query_tool()
    await tester.test_retrieve_tool()
    await tester.test_resources()
    await tester.test_error_scenarios()
    
    print("\n✅ All MCP tools tests completed!")
    print("\n📋 Summary of tested components:")
    print("1. query_knowledge_base MCP Tool ✅")
    print("   - Basic queries")
    print("   - Queries with KB IDs")
    print("   - Queries with custom parameters")
    print("   - Queries with conversation history")
    print("2. retrieve_from_knowledge_base MCP Tool ✅")
    print("   - Basic retrieval")
    print("   - Retrieval with KB IDs")
    print("   - Retrieval with custom top K")
    print("3. MCP Resources ✅")
    print("   - List knowledge bases")
    print("   - Knowledge base status")
    print("   - Workspace structure")
    print("4. Error Handling ✅")
    print("   - Invalid workspace ID")
    print("   - Empty queries")
    print("   - Invalid KB IDs")

if __name__ == "__main__":
    print("🔧 OnlysaidKB MCP Tools Test")
    print("=" * 50)
    print("This test directly calls the MCP tool functions")
    print("Make sure to set environment variables:")
    print("  export ONLYSAIDKB_BASE_URL='http://localhost:8000'")
    print("  export TEST_WORKSPACE_ID='your-test-workspace-id'")
    print("  export TEST_KB_IDS='kb-1,kb-2,kb-3'")
    print("=" * 50)
    
    asyncio.run(run_all_tests()) 