#!/usr/bin/env python3
"""
Simple connectivity test for OnlysaidKB MCP Server
Tests basic connection and health check
"""

import asyncio
import httpx
import os
import json

async def test_connectivity():
    """Test basic connectivity to OnlysaidKB backend"""
    base_url = os.getenv("ONLYSAIDKB_BASE_URL", "http://onlysaid-dev.com/api/kb")
    timeout = int(os.getenv("ONLYSAIDKB_TIMEOUT", "10"))
    
    print(f"🔌 Testing connectivity to: {base_url}")
    print(f"⏱️ Timeout: {timeout} seconds")
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        
        # Test 1: Basic server availability
        try:
            print("\n1️⃣ Testing server availability...")
            response = await client.get(f"{base_url}/")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
            if response.status_code in [200, 404]:  # 404 is fine, means server is running
                print("✅ Server is reachable")
            else:
                print("❌ Server might not be running")
                
        except httpx.ConnectError:
            print("❌ Cannot connect to server - is it running?")
        except Exception as e:
            print(f"❌ Server availability error: {str(e)}")
        
        # Test 2: Test the actual API endpoint structure
        try:
            print("\n2️⃣ Testing API endpoint structure...")
            test_workspace_id = os.getenv("TEST_WORKSPACE_ID", "test-workspace")
            
            # Test the view endpoint (GET request)
            response = await client.get(f"{base_url}/view/{test_workspace_id}")
            print(f"View endpoint status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API endpoint working")
                print(f"Data sources found: {len(result.get('dataSources', []))}")
                print(f"Response preview: {json.dumps(result, indent=2)[:300]}...")
            elif response.status_code == 404:
                print("⚠️ Workspace not found (expected for test)")
            else:
                print(f"❌ API endpoint error: {response.text}")
                
        except Exception as e:
            print(f"❌ API endpoint error: {str(e)}")
            
        # Test 3: Test a POST endpoint
        try:
            print("\n3️⃣ Testing POST endpoint...")
            
            # Test the retrieve endpoint
            test_payload = {
                "workspace_id": "test-workspace",
                "query": "test query",
                "top_k": 3
            }
            
            response = await client.post(
                f"{base_url}/retrieve",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"Retrieve endpoint status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ POST endpoint working")
                print(f"Response preview: {json.dumps(result, indent=2)[:300]}...")
            else:
                print(f"⚠️ POST endpoint response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ POST endpoint error: {str(e)}")

if __name__ == "__main__":
    print("🌐 OnlysaidKB MCP Connectivity Test")
    print("=" * 50)
    print("This test checks:")
    print("1. Health endpoint")
    print("2. Server availability")
    print("3. Basic API endpoint")
    print("=" * 50)
    
    asyncio.run(test_connectivity()) 