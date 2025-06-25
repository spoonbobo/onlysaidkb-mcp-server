#!/usr/bin/env python

import os
import json
import sys
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import httpx

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed, environment variables won't be loaded from .env file")

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("OnlysaidKB MCP")
except ImportError:
    print("Warning: MCP not installed, server functionality will be limited")
    mcp = None

@dataclass
class OnlysaidKBConfig:
    base_url: str = os.getenv("ONLYSAIDKB_BASE_URL", "http://onlysaid-dev.com/api/kb")
    default_model: str = os.getenv("ONLYSAIDKB_DEFAULT_MODEL", "gpt-4")
    default_top_k: int = int(os.getenv("ONLYSAIDKB_DEFAULT_TOP_K", "5"))
    default_language: str = os.getenv("ONLYSAIDKB_DEFAULT_LANGUAGE", "en")
    timeout: int = int(os.getenv("ONLYSAIDKB_TIMEOUT", "30"))

config = OnlysaidKBConfig()

async def make_api_request(endpoint: str, data: Optional[Dict[str, Any]] = None, method: str = "POST") -> Dict[str, Any]:
    """Make API request to OnlysaidKB backend"""
    url = f"{config.base_url}{endpoint}"
    
    async with httpx.AsyncClient(timeout=config.timeout) as client:
        if method.upper() == "GET":
            response = await client.get(
                url,
                headers={"Accept": "application/json"}
            )
        else:
            response = await client.post(
                url,
                json=data,
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
        response.raise_for_status()
        return response.json()

@mcp.tool(description="Query knowledge bases with natural language and get AI-generated answers")
async def query_knowledge_base(
    workspace_id: str,
    query: str,
    knowledge_bases: Optional[List[str]] = None,
    model: Optional[str] = None,
    conversation_history: Optional[List[str]] = None,
    top_k: Optional[int] = None,
    preferred_language: Optional[str] = None,
    message_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query knowledge bases and get AI-generated answers based on retrieved documents.
    
    This tool performs both retrieval and generation - it finds relevant documents
    from the knowledge bases and then uses an AI model to generate a comprehensive
    answer based on those documents.
    
    Parameters:
    - workspace_id: The workspace ID containing the knowledge bases
    - query: The natural language query to ask
    - knowledge_bases: List of knowledge base IDs to search in (optional, searches all if not provided)
    - model: AI model to use for generation (optional, uses default if not provided)
    - conversation_history: Previous conversation context as list of strings (optional)
    - top_k: Number of top documents to retrieve (optional, defaults to 5)
    - preferred_language: Preferred language for the response (optional, defaults to 'en')
    - message_id: Message ID for tracking (optional)
    
    Returns:
    - Complete AI-generated answer with source information (non-streaming)
    """
    
    # Prepare the payload matching the actual Python API (QueryRequest schema)
    # MCP tools always use non-streaming mode for synchronous responses
    payload = {
        "workspace_id": workspace_id,
        "query": query,
        "streaming": False,
    }
    
    # Add optional parameters if provided
    if knowledge_bases:
        payload["knowledge_bases"] = knowledge_bases
    if conversation_history:
        payload["conversation_history"] = conversation_history
    if top_k:
        payload["top_k"] = top_k
    if model:
        payload["model"] = model
    if preferred_language:
        payload["preferred_language"] = preferred_language
    if message_id:
        payload["message_id"] = message_id
    
    try:
        result = await make_api_request("/query", payload)
        
        # Add debug information
        result["_debug"] = {
            "query_parameters": payload,
            "endpoint_used": "/query",
            "config_used": {
                "base_url": config.base_url,
                "default_model": config.default_model,
                "default_top_k": config.default_top_k,
                "default_language": config.default_language
            }
        }
        
        return result
        
    except httpx.HTTPStatusError as e:
        error_result = {
            "error": f"HTTP {e.response.status_code}: {e.response.text}",
            "status_code": e.response.status_code,
            "_debug": {
                "query_parameters": payload,
                "endpoint_used": "/query",
                "error_type": "http_error"
            }
        }
        return error_result
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "_debug": {
                "query_parameters": payload,
                "endpoint_used": "/query",
                "error_type": "general_error"
            }
        }
        return error_result

@mcp.tool(description="Retrieve relevant documents from knowledge bases without AI generation")
async def retrieve_from_knowledge_base(
    workspace_id: str,
    query: str,
    knowledge_bases: Optional[List[str]] = None,
    top_k: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieve relevant documents from knowledge bases without AI generation.
    
    This tool performs pure document retrieval - it finds and returns the most
    relevant documents from the knowledge bases based on semantic similarity,
    but does not generate an AI answer. Use this when you want raw document
    content or when you plan to process the documents yourself.
    
    Parameters:
    - workspace_id: The workspace ID containing the knowledge bases
    - query: The search query to find relevant documents
    - knowledge_bases: List of knowledge base IDs to search in (optional, searches all if not provided)
    - top_k: Number of top documents to retrieve (optional, defaults to 5)
    
    Returns:
    - List of retrieved documents with scores, sources, and metadata
    """
    
    # Prepare the payload for retrieval
    payload = {
        "workspace_id": workspace_id,
        "query": query,
        "top_k": top_k or config.default_top_k,
    }
    
    # Add optional parameters if provided
    if knowledge_bases:
        payload["knowledge_bases"] = knowledge_bases
    
    try:
        result = await make_api_request("/retrieve", payload)
        
        # Add debug information
        result["_debug"] = {
            "retrieval_parameters": payload,
            "endpoint_used": "/retrieve",
            "config_used": {
                "base_url": config.base_url,
                "default_top_k": config.default_top_k
            }
        }
        
        return result
        
    except httpx.HTTPStatusError as e:
        error_result = {
            "error": f"HTTP {e.response.status_code}: {e.response.text}",
            "status_code": e.response.status_code,
            "_debug": {
                "retrieval_parameters": payload,
                "endpoint_used": "/retrieve",
                "error_type": "http_error"
            }
        }
        return error_result
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "_debug": {
                "retrieval_parameters": payload,
                "endpoint_used": "/retrieve",
                "error_type": "general_error"
            }
        }
        return error_result

# Resources for easy data access
@mcp.resource("onlysaidkb://workspace/{workspace_id}/knowledge_bases")
async def list_knowledge_bases_resource(workspace_id: str) -> str:
    """
    Resource that returns the list of knowledge bases in a workspace.
    
    Parameters:
    - workspace_id: The workspace ID
    """
    try:
        # Use the view endpoint to get data sources (knowledge bases)
        result = await make_api_request(f"/view/{workspace_id}", method="GET")
        # Extract just the data sources for this resource
        kb_list = result.get("dataSources", [])
        return json.dumps(kb_list, indent=2)
    except Exception as e:
        return f"Error retrieving knowledge bases: {str(e)}"

@mcp.resource("onlysaidkb://workspace/{workspace_id}/kb/{kb_id}/status")
async def knowledge_base_status_resource(workspace_id: str, kb_id: str) -> str:
    """
    Resource that returns the status of a specific knowledge base.
    
    Parameters:
    - workspace_id: The workspace ID
    - kb_id: The knowledge base ID
    """
    try:
        result = await make_api_request(f"/kb_status/{workspace_id}/{kb_id}", method="GET")
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error retrieving knowledge base status: {str(e)}"

@mcp.resource("onlysaidkb://workspace/{workspace_id}/structure")
async def workspace_structure_resource(workspace_id: str) -> str:
    """
    Resource that returns the structure of all knowledge bases in a workspace.
    
    Parameters:
    - workspace_id: The workspace ID
    """
    try:
        result = await make_api_request(f"/view/{workspace_id}", method="GET")
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error retrieving workspace structure: {str(e)}"

if __name__ == "__main__":
    print(f"🚀 Starting OnlysaidKB MCP Server...")
    mcp.run() 