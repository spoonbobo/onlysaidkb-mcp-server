#!/usr/bin/env python3
"""
Test OnlysaidKB API using the MCP server implementation
Comprehensive tests for query and retrieve operations
"""

import asyncio
import httpx
import json
import os
from typing import Dict, Any, List, Optional

class OnlysaidKBTestClient:
    def __init__(self):
        self.base_url = os.getenv("ONLYSAIDKB_BASE_URL", "http://onlysaid-dev.com")
        self.default_model = os.getenv("ONLYSAIDKB_DEFAULT_MODEL", "gpt-4")
        self.default_top_k = int(os.getenv("ONLYSAIDKB_DEFAULT_TOP_K", "5"))
        self.default_language = os.getenv("ONLYSAIDKB_DEFAULT_LANGUAGE", "en")
        self.timeout = int(os.getenv("ONLYSAIDKB_TIMEOUT", "30"))
        
        # Test workspace and knowledge base IDs
        self.test_workspace_id = os.getenv("TEST_WORKSPACE_ID", "test-workspace-123")
        self.test_kb_ids = os.getenv("TEST_KB_IDS", "kb-1,kb-2").split(",")
        
        self.session = None
        
        print(f"🔧 OnlysaidKB Test Client Configuration:")
        print(f"  Base URL: {self.base_url}")
        print(f"  Default Model: {self.default_model}")
        print(f"  Default Top K: {self.default_top_k}")
        print(f"  Default Language: {self.default_language}")
        print(f"  Test Workspace ID: {self.test_workspace_id}")
        print(f"  Test KB IDs: {self.test_kb_ids}")
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def make_api_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request to OnlysaidKB backend"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = await self.session.post(
                url,
                json=data,
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            
            print(f"🔄 API Request: {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {endpoint}")
                return result
            else:
                print(f"❌ API Error: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
                
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return {"error": str(e)}
    
    # Test 1: List Knowledge Bases
    async def test_list_knowledge_bases(self) -> Dict[str, Any]:
        """Test listing knowledge bases in a workspace"""
        print(f"📚 Testing list knowledge bases for workspace: {self.test_workspace_id}")
        
        # Use the actual API endpoint structure
        url = f"{self.base_url}/api/view/{self.test_workspace_id}"
        
        try:
            response = await self.session.get(url)
            print(f"🔄 List KB Request - Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                data_sources = result.get("dataSources", [])
                print(f"✅ Success: Listed {len(data_sources)} knowledge bases")
                return result
            else:
                print(f"❌ List KB Error: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
                
        except Exception as e:
            print(f"❌ List KB Request failed: {str(e)}")
            return {"error": str(e)}
    
    # Test 2: Knowledge Base Status
    async def test_kb_status(self, kb_id: str) -> Dict[str, Any]:
        """Test getting knowledge base status"""
        print(f"📊 Testing KB status for: {kb_id}")
        
        url = f"{self.base_url}/api/kb_status/{self.test_workspace_id}/{kb_id}"
        
        try:
            response = await self.session.get(url)
            print(f"🔄 KB Status Request - Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: Got KB status")
                return result
            else:
                print(f"❌ KB Status Error: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
                
        except Exception as e:
            print(f"❌ KB Status Request failed: {str(e)}")
            return {"error": str(e)}
    
    # Test 3: Query Knowledge Base (Main Tool)
    async def test_query_knowledge_base(
        self,
        query: str,
        knowledge_bases: Optional[List[str]] = None,
        model: Optional[str] = None,
        conversation_history: Optional[List[str]] = None,
        top_k: Optional[int] = None,
        preferred_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Test querying knowledge bases with AI generation"""
        print(f"🤖 Testing query knowledge base: '{query[:50]}...'")
        
        # Prepare payload matching the server implementation (non-streaming for MCP)
        payload = {
            "workspace_id": self.test_workspace_id,
            "query": query,
            "streaming": False,
            "model": model or self.default_model,
            "top_k": top_k or self.default_top_k,
            "preferred_language": preferred_language or self.default_language,
        }
        
        # Add optional parameters
        if knowledge_bases:
            payload["knowledge_bases"] = knowledge_bases
        if conversation_history:
            payload["conversation_history"] = conversation_history
        
        print(f"📤 Query payload: {json.dumps(payload, indent=2)}")
        
        return await self.make_api_request("/api/query", payload)
    
    # Test 4: Retrieve from Knowledge Base (Main Tool)
    async def test_retrieve_from_knowledge_base(
        self,
        query: str,
        knowledge_bases: Optional[List[str]] = None,
        top_k: Optional[int] = None
    ) -> Dict[str, Any]:
        """Test retrieving documents without AI generation"""
        print(f"🔍 Testing retrieve from knowledge base: '{query[:50]}...'")
        
        # Prepare payload for retrieval
        payload = {
            "workspace_id": self.test_workspace_id,
            "query": query,
            "top_k": top_k or self.default_top_k,
        }
        
        # Add optional parameters
        if knowledge_bases:
            payload["knowledge_bases"] = knowledge_bases
        
        print(f"📤 Retrieve payload: {json.dumps(payload, indent=2)}")
        
        return await self.make_api_request("/api/retrieve", payload)
    
    # Test 5: View Workspace Structure
    async def test_view_workspace_structure(self, kb_id: Optional[str] = None) -> Dict[str, Any]:
        """Test viewing workspace/KB structure"""
        print(f"🏗️ Testing view workspace structure")
        
        url = f"{self.base_url}/api/view/{self.test_workspace_id}"
        if kb_id:
            url += f"?kb_id={kb_id}"
        
        try:
            response = await self.session.get(url)
            print(f"🔄 View Structure Request - Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: Got workspace structure")
                return result
            else:
                print(f"❌ View Structure Error: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
                
        except Exception as e:
            print(f"❌ View Structure Request failed: {str(e)}")
            return {"error": str(e)}

async def test_all_onlysaidkb_operations():
    """Test all OnlysaidKB operations"""
    print("🚀 Testing OnlysaidKB MCP Operations...")
    print("=" * 80)
    
    async with OnlysaidKBTestClient() as client:
        
        # Test 1: List Knowledge Bases
        print("\n1️⃣ Testing List Knowledge Bases...")
        list_result = await client.test_list_knowledge_bases()
        print(f"📊 List KB result: {json.dumps(list_result, indent=2)}")
        
        # Test 2: Knowledge Base Status (if we have KB IDs)
        if client.test_kb_ids and client.test_kb_ids[0]:
            print(f"\n2️⃣ Testing KB Status for: {client.test_kb_ids[0]}...")
            status_result = await client.test_kb_status(client.test_kb_ids[0])
            print(f"📊 KB Status result: {json.dumps(status_result, indent=2)}")
        
        # Test 3: View Workspace Structure
        print("\n3️⃣ Testing View Workspace Structure...")
        structure_result = await client.test_view_workspace_structure()
        print(f"📊 Workspace Structure result: {json.dumps(structure_result, indent=2)}")
        
        # Test 4: Query Knowledge Base (Main Tool Test)
        print("\n4️⃣ Testing Query Knowledge Base...")
        
        # Test queries
        test_queries = [
            "What is the main purpose of this system?",
            "How do I configure the knowledge base?",
            "What are the API endpoints available?",
            "Tell me about the authentication process"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n  4.{i} Query: '{query}'")
            query_result = await client.test_query_knowledge_base(
                query=query,
                knowledge_bases=client.test_kb_ids if client.test_kb_ids[0] else None,
                top_k=3  # Limit for testing
            )
            print(f"📊 Query result: {json.dumps(query_result, indent=2)}")
            
            # Brief pause between queries
            await asyncio.sleep(1)
        
        # Test 5: Retrieve from Knowledge Base (Main Tool Test)
        print("\n5️⃣ Testing Retrieve from Knowledge Base...")
        
        # Test retrieval queries
        retrieval_queries = [
            "system configuration",
            "API documentation",
            "user authentication",
            "database schema"
        ]
        
        for i, query in enumerate(retrieval_queries, 1):
            print(f"\n  5.{i} Retrieval: '{query}'")
            retrieve_result = await client.test_retrieve_from_knowledge_base(
                query=query,
                knowledge_bases=client.test_kb_ids if client.test_kb_ids[0] else None,
                top_k=5
            )
            print(f"📊 Retrieve result: {json.dumps(retrieve_result, indent=2)}")
            
            # Brief pause between retrievals
            await asyncio.sleep(1)
        
        # Test 6: Query with Conversation History
        print("\n6️⃣ Testing Query with Conversation History...")
        conversation_history = [
            "user: What is this system about?",
            "assistant: This is a knowledge base system for managing and querying documents.",
            "user: How do I add new documents?"
        ]
        
        history_query_result = await client.test_query_knowledge_base(
            query="What are the supported file formats?",
            conversation_history=conversation_history,
            top_k=3
        )
        print(f"📊 Query with History result: {json.dumps(history_query_result, indent=2)}")
        
        print("\n✅ All OnlysaidKB operations tested!")
        print("\n📋 Summary of tested operations:")
        print("1. List Knowledge Bases ✅")
        print("2. Knowledge Base Status ✅")
        print("3. View Workspace Structure ✅")
        print("4. Query Knowledge Base (Main Tool) ✅")
        print("   - Multiple test queries")
        print("   - With specific KB IDs")
        print("   - With conversation history")
        print("5. Retrieve from Knowledge Base (Main Tool) ✅")
        print("   - Multiple retrieval queries")
        print("   - Pure document retrieval")

async def test_error_handling():
    """Test error handling scenarios"""
    print("\n🚨 Testing Error Handling Scenarios...")
    print("=" * 50)
    
    async with OnlysaidKBTestClient() as client:
        
        # Test 1: Invalid workspace ID
        print("\n1️⃣ Testing Invalid Workspace ID...")
        client.test_workspace_id = "invalid-workspace-id"
        
        invalid_result = await client.test_query_knowledge_base(
            query="Test query with invalid workspace"
        )
        print(f"📊 Invalid Workspace result: {json.dumps(invalid_result, indent=2)}")
        
        # Test 2: Empty query
        print("\n2️⃣ Testing Empty Query...")
        client.test_workspace_id = os.getenv("TEST_WORKSPACE_ID", "test-workspace-123")  # Reset
        
        empty_query_result = await client.test_query_knowledge_base(
            query=""
        )
        print(f"📊 Empty Query result: {json.dumps(empty_query_result, indent=2)}")
        
        # Test 3: Invalid knowledge base IDs
        print("\n3️⃣ Testing Invalid Knowledge Base IDs...")
        
        invalid_kb_result = await client.test_query_knowledge_base(
            query="Test query with invalid KB IDs",
            knowledge_bases=["invalid-kb-1", "invalid-kb-2"]
        )
        print(f"📊 Invalid KB IDs result: {json.dumps(invalid_kb_result, indent=2)}")
        
        print("\n✅ Error handling tests completed!")

if __name__ == "__main__":
    print("🌍 OnlysaidKB MCP Test Suite")
    print("=" * 80)
    print("Testing these operations:")
    print("1. List Knowledge Bases")
    print("2. Knowledge Base Status")
    print("3. View Workspace Structure")
    print("4. Query Knowledge Base (Main MCP Tool)")
    print("5. Retrieve from Knowledge Base (Main MCP Tool)")
    print("6. Query with Conversation History")
    print("7. Error Handling Scenarios")
    print("=" * 80)
    print("Set these environment variables for testing:")
    print("  export ONLYSAIDKB_BASE_URL='http://localhost:8000'")
    print("  export TEST_WORKSPACE_ID='your-test-workspace-id'")
    print("  export TEST_KB_IDS='kb-1,kb-2,kb-3'")
    print("=" * 80)
    
    # Run main tests
    asyncio.run(test_all_onlysaidkb_operations())
    
    # Run error handling tests
    asyncio.run(test_error_handling()) 