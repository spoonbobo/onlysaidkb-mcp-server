#!/usr/bin/env python
import sys
import os
from onlysaidkb_mcp.server import mcp

def setup_environment():
    """Setup and validate environment configuration"""
    print("[CONFIG] OnlysaidKB MCP Server Configuration:")
    
    # Check required environment variables
    required_vars = ["ONLYSAIDKB_BASE_URL"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"  {var}: {value}")
    
    if missing_vars:
        print(f"[ERROR] Missing required environment variables: {', '.join(missing_vars)}")
        print("\n[INFO] Set these environment variables:")
        print("  export ONLYSAIDKB_BASE_URL='http://localhost:8000'  # Your OnlysaidKB API base URL")
        print("  export ONLYSAIDKB_DEFAULT_MODEL='gpt-4'  # Optional, default model")
        print("  export ONLYSAIDKB_DEFAULT_TOP_K='5'  # Optional, default top K results")
        print("  export ONLYSAIDKB_DEFAULT_LANGUAGE='en'  # Optional, default language")
        return False
    
    # Display optional configuration
    optional_vars = ["ONLYSAIDKB_DEFAULT_MODEL", "ONLYSAIDKB_DEFAULT_TOP_K", "ONLYSAIDKB_DEFAULT_LANGUAGE"]
    for var in optional_vars:
        value = os.getenv(var, "default")
        print(f"  {var}: {value}")
    
    return True

def run_server():
    """Main entry point for the OnlysaidKB MCP Server"""
    if not setup_environment():
        sys.exit(1)
    
    print("\n[START] Starting OnlysaidKB MCP Server...")
    print("[MODE] Running server in standard mode...")
    print("[OPS] Available operations: query_knowledge_base, retrieve_from_knowledge_base")
    
    # Run the server with the stdio transport
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run_server() 