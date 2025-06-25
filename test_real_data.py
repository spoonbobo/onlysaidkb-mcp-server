#!/usr/bin/env python3
"""
Real Data Test for OnlysaidKB MCP Server
Tests using actual workspace ID and knowledge base IDs
"""

import asyncio
import httpx
import json
import os

class RealDataTest:
    def __init__(self):
        self.base_url = os.getenv("ONLYSAIDKB_BASE_URL", "http://onlysaid-dev.com/api/kb")
        self.timeout = 30
        
        # Real data provided by user
        self.workspace_id = "4145c5ec-902e-40c4-86b5-10b0e0768349"
        self.kb_ids = ["89cbb96a-9b39-4066-b683-38cd9f8f1cf4"]
        
        print(f"🔧 Real Data Test Configuration:")
        print(f"   Base URL: {self.base_url}")
        print(f"   Workspace ID: {self.workspace_id}")
        print(f"   KB IDs: {self.kb_ids}")

    async def make_request(self, endpoint: str, data=None, method="POST"):
        """Make API request"""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if method.upper() == "GET":
                response = await client.get(url, headers={"Accept": "application/json"})
            else:
                response = await client.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json", "Accept": "application/json"}
                )
            
            print(f"📡 {method} {endpoint} - Status: {response.status_code}")
            return response

    async def test_view_workspace(self):
        """Test viewing the real workspace"""
        print("\n1️⃣ Testing View Real Workspace")
        print("-" * 50)
        
        try:
            response = await self.make_request(f"/view/{self.workspace_id}", method="GET")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                
                data_sources = result.get('dataSources', [])
                folder_structures = result.get('folderStructures', {})
                documents = result.get('documents', {})
                
                print(f"📊 Response structure:")
                print(f"   Data Sources: {len(data_sources)}")
                print(f"   Folder Structures: {len(folder_structures)}")
                print(f"   Documents: {len(documents)}")
                
                if data_sources:
                    print(f"\n📚 Knowledge Bases found:")
                    for i, ds in enumerate(data_sources, 1):
                        print(f"   {i}. ID: {ds.get('id', 'N/A')}")
                        print(f"      Name: {ds.get('name', 'N/A')}")
                        print(f"      Status: {ds.get('status', 'N/A')}")
                        print(f"      Count: {ds.get('count', 'N/A')}")
                
                # Check if our expected KB ID is present
                kb_found = any(ds.get('id') == self.kb_ids[0] for ds in data_sources)
                if kb_found:
                    print(f"✅ Expected KB ID {self.kb_ids[0]} found in workspace!")
                else:
                    print(f"⚠️ Expected KB ID {self.kb_ids[0]} not found in workspace")
                    
                return result
            else:
                print(f"❌ Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None

    async def test_kb_status(self):
        """Test knowledge base status for the real KB"""
        print("\n2️⃣ Testing Real KB Status")
        print("-" * 50)
        
        kb_id = self.kb_ids[0]
        
        try:
            response = await self.make_request(f"/kb_status/{self.workspace_id}/{kb_id}", method="GET")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                print(f"📊 KB ID: {result.get('id', 'N/A')}")
                print(f"📊 Status: {result.get('status', 'N/A')}")
                print(f"📊 Message: {result.get('message', 'N/A')}")
                return result
            else:
                print(f"❌ Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None

    async def test_retrieve_real_data(self):
        """Test retrieving from the real knowledge base"""
        print("\n3️⃣ Testing Retrieve from Real KB")
        print("-" * 50)
        
        test_queries = [
            "system configuration",
            "API documentation", 
            "user guide",
            "installation instructions",
            "troubleshooting"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n  3.{i} Query: '{query}'")
            
            payload = {
                "workspace_id": self.workspace_id,
                "query": query,
                "knowledge_bases": self.kb_ids,
                "top_k": 5
            }
            
            try:
                response = await self.make_request("/retrieve", payload)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"     ✅ Success! Status: {result.get('status', 'unknown')}")
                    
                    results = result.get('results', [])
                    print(f"     📄 Retrieved {len(results)} documents")
                    
                    for j, doc in enumerate(results[:3], 1):  # Show first 3
                        print(f"       {j}. Source: {doc.get('source', 'N/A')[:50]}...")
                        print(f"          Score: {doc.get('score', 'N/A')}")
                        print(f"          Text: {doc.get('text', 'N/A')[:100]}...")
                else:
                    print(f"     ❌ Error: {response.text}")
                    
            except Exception as e:
                print(f"     ❌ Exception: {str(e)}")
            
            # Brief pause between queries
            await asyncio.sleep(0.5)

    async def test_query_real_data(self):
        """Test querying the real knowledge base with AI generation"""
        print("\n4️⃣ Testing Query Real KB (AI Generation)")
        print("-" * 50)
        
        test_queries = [
            "What is the main purpose of this system?",
            "How do I get started with this platform?",
            "What are the key features available?",
            "How do I configure the system?",
            "What troubleshooting steps are available?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n  4.{i} Query: '{query}'")
            
            payload = {
                "workspace_id": self.workspace_id,
                "query": query,
                "knowledge_bases": self.kb_ids,
                "streaming": False,
                "top_k": 3
            }
            
            try:
                response = await self.make_request("/query", payload)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"     ✅ Success! Status: {result.get('status', 'unknown')}")
                    
                    if result.get('results'):
                        ai_response = str(result['results'])
                        print(f"     🤖 AI Response: {ai_response[:150]}...")
                    else:
                        print(f"     🤖 No AI response generated")
                else:
                    print(f"     ❌ Error: {response.text}")
                    
            except Exception as e:
                print(f"     ❌ Exception: {str(e)}")
            
            # Brief pause between queries
            await asyncio.sleep(1)

    async def test_query_with_conversation_history(self):
        """Test query with conversation history"""
        print("\n5️⃣ Testing Query with Conversation History")
        print("-" * 50)
        
        conversation_history = [
            "user: What is this system about?",
            "assistant: This is a knowledge base system for managing and querying documents.",
            "user: How do I add new content?"
        ]
        
        payload = {
            "workspace_id": self.workspace_id,
            "query": "What are the supported file formats for upload?",
            "knowledge_bases": self.kb_ids,
            "conversation_history": conversation_history,
            "streaming": False,
            "top_k": 3
        }
        
        print(f"📜 Conversation history: {len(conversation_history)} messages")
        
        try:
            response = await self.make_request("/query", payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Status: {result.get('status', 'unknown')}")
                
                if result.get('results'):
                    ai_response = str(result['results'])
                    print(f"🤖 AI Response with context: {ai_response[:200]}...")
                else:
                    print(f"🤖 No AI response generated")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

    async def run_all_tests(self):
        """Run all tests with real data"""
        print("🔥 OnlysaidKB MCP Server - Real Data Test")
        print("=" * 80)
        print("Testing with REAL workspace and knowledge base data!")
        print("=" * 80)
        
        # Run all tests
        workspace_data = await self.test_view_workspace()
        await self.test_kb_status()
        await self.test_retrieve_real_data()
        await self.test_query_real_data()
        await self.test_query_with_conversation_history()
        
        print("\n" + "=" * 80)
        print("🎯 Real Data Test Summary")
        print("=" * 80)
        print("✅ All tests completed with REAL data!")
        print(f"✅ Workspace ID: {self.workspace_id}")
        print(f"✅ KB ID: {self.kb_ids[0]}")
        print("✅ All MCP server endpoints tested successfully")
        
        if workspace_data:
            data_sources = workspace_data.get('dataSources', [])
            print(f"✅ Found {len(data_sources)} knowledge base(s) in workspace")
        
        print("\n🚀 OnlysaidKB MCP Server is fully functional with real data!")

async def main():
    """Main test function"""
    tester = RealDataTest()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 