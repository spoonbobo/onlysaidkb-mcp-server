# OnlysaidKB MCP Server

A Model Context Protocol (MCP) server implementation that provides tools and resources for interacting with OnlysaidKB (Knowledge Base) system via its API.

## Features

This MCP server provides comprehensive tools for OnlysaidKB integration:

### Knowledge Base Operations
- **query_knowledge_base**: Query knowledge bases with AI-generated answers
- **retrieve_from_knowledge_base**: Pure document retrieval without AI generation

### System Information
- **workspace_structure**: View workspace structure and list knowledge bases
- **knowledge_base_status**: Get knowledge base status information

### Resources
- `onlysaidkb://workspace/{workspace_id}/knowledge_bases` - List all knowledge bases in a workspace
- `onlysaidkb://workspace/{workspace_id}/kb/{kb_id}/status` - Get knowledge base status
- `onlysaidkb://workspace/{workspace_id}/structure` - View workspace structure

## Installation

### Prerequisites
- Python 3.10 or higher
- A running OnlysaidKB instance
- Access to the OnlysaidKB API endpoints

### Setup

1. Clone or download this MCP server
2. Install dependencies using UV:
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -e .
   ```

### Environment Configuration

Set the required environment variables:

```bash
# Required
export ONLYSAIDKB_BASE_URL="http://onlysaid-dev.com/api/kb"

# Optional
export ONLYSAIDKB_TIMEOUT="30"  # Request timeout in seconds
```

Or for PowerShell:
```powershell
$env:ONLYSAIDKB_BASE_URL="http://onlysaid-dev.com/api/kb"
```

You can also copy `env.example` to `.env` and modify it with your configuration.

### OnlysaidKB Configuration

1. **Ensure Knowledge Base Service is Running**:
   - Verify your OnlysaidKB backend is accessible
   - Check that the API endpoints are available

2. **Configure Workspace Access**:
   - Ensure you have valid workspace IDs
   - Verify knowledge bases are properly registered

## Usage

### Running the Server

Using UV:
```bash
uv run src/onlysaidkb_mcp/main.py
```

Or using Python:
```bash
python -m onlysaidkb_mcp.main
```

### Integration with MCP Clients

#### For Claude Desktop

Set the required environment variables:

```bash
export ONLYSAIDKB_BASE_URL="http://onlysaid-dev.com/api/kb"
export ONLYSAIDKB_TIMEOUT="30"
```

Then edit your Claude Desktop config file and add the server configuration:

```json
{
  "mcpServers": {
    "onlysaidkb": {
      "command": "uv",
      "args": [
        "--directory",
        "<full path to onlysaidkb-mcp-server directory>",
        "run",
        "src/onlysaidkb_mcp/main.py"
      ],
      "env": {
        "ONLYSAIDKB_BASE_URL": "http://onlysaid-dev.com/api/kb",
        "ONLYSAIDKB_TIMEOUT": "30"
      }
    }
  }
}
```

> **Note**: Replace `<full path to onlysaidkb-mcp-server directory>` with the actual full path to where you cloned/downloaded this repository. You can find this path by navigating to the directory and running `pwd` (on macOS/Linux) or `cd` (on Windows).

#### For OnlySaid Electron App

When configuring the OnlysaidKB MCP Server in the OnlySaid Electron app:

1. **OnlysaidKB MCP Server Path**: Enter the full path to the onlysaidkb-mcp-server directory
2. **OnlysaidKB Base URL**: Enter your OnlysaidKB API base URL (e.g., `http://onlysaid-dev.com/api/kb`)
3. **Request Timeout**: Optional timeout in seconds (default: 30)

### Example Usage

#### Query Knowledge Base with AI Generation
```python
# Basic query (always non-streaming for MCP)
result = await query_knowledge_base(
    workspace_id="my-workspace",
    query="What is the main purpose of this system?"
)
print(f"Answer: {result['results']}")
```

#### Query with Specific Knowledge Bases
```python
# Query specific knowledge bases
result = await query_knowledge_base(
    workspace_id="my-workspace",
    query="How do I configure authentication?",
    knowledge_bases=["kb-1", "kb-2"],
    top_k=3
)
```

#### Query with Conversation History
```python
# Query with conversation context
result = await query_knowledge_base(
    workspace_id="my-workspace",
    query="What about the API endpoints?",
    conversation_history=[
        "user: What is this system?",
        "assistant: This is a knowledge base system.",
        "user: How do I use it?"
    ]
)
```

#### Retrieve Documents Only
```python
# Basic document retrieval without AI generation
result = await retrieve_from_knowledge_base(
    workspace_id="my-workspace",
    query="system configuration",
    top_k=10
)

for doc in result['results']:
    print(f"Source: {doc['source']}")
    print(f"Score: {doc['score']}")
    print(f"Text: {doc['text'][:100]}...")
```

#### Retrieve from Specific Knowledge Bases
```python
# Retrieval from specific knowledge bases
result = await retrieve_from_knowledge_base(
    workspace_id="my-workspace",
    query="API documentation",
    knowledge_bases=["docs-kb", "api-kb"]
)
```

## API Functions

### Authentication
All API requests are made to the configured base URL. No additional authentication is required beyond network access to the OnlysaidKB service.

### Error Handling
The server includes comprehensive error handling and will return detailed error messages for debugging. All responses include debug information for troubleshooting.

### Query Processing
- **AI Generation**: The `query_knowledge_base` tool performs both document retrieval and AI-powered answer generation
- **Document Retrieval**: The `retrieve_from_knowledge_base` tool returns raw documents with similarity scores
- **Streaming Support**: MCP tools always use non-streaming mode for synchronous responses

## Development

### Project Structure
```
onlysaidkb-mcp-server/
├── src/onlysaidkb_mcp/
│   ├── __init__.py
│   ├── server.py      # Main server implementation
│   └── main.py        # Entry point
├── tests/
│   ├── connectivity_test.py
│   ├── test_onlysaidkb_api.py
│   └── mcp_tools_test.py
├── pyproject.toml     # Project configuration
└── README.md         # This file
```

### Adding New Tools
To add new OnlysaidKB API functions:

1. Add the function to `server.py` using the `@mcp.tool` decorator
2. Use `make_api_request()` for API calls
3. Add appropriate error handling and debug information
4. Update the available operations list in this README

### Testing

The project includes comprehensive tests:

```bash
# Run all tests
uv run pytest tests/ -v

# Run connectivity tests
uv run python tests/connectivity_test.py

# Run API tests
uv run python tests/test_onlysaidkb_api.py

# Run MCP tools tests
uv run python tests/mcp_tools_test.py
```

Set up a test environment with:
- A running OnlysaidKB development instance
- Test workspace with sample knowledge bases
- Sample documents and content for testing

Test files included:
- `connectivity_test.py` - Basic connectivity and import tests
- `test_onlysaidkb_api.py` - Comprehensive API functionality tests
- `mcp_tools_test.py` - Direct MCP tool function testing

## Troubleshooting

### Common Issues

1. **Connection Errors**: 
   - Run the diagnostic tool: `uv run python tests/connectivity_test.py`
   - Check that OnlysaidKB service is running and accessible
   - Verify the base URL is correct and includes the `/api/kb` prefix

2. **Query Failures**: 
   - Ensure workspace ID exists and has knowledge bases
   - Check that knowledge bases are properly registered and running
   - Verify query parameters are valid

3. **Empty Results**: 
   - Check if knowledge bases contain relevant documents
   - Verify knowledge base IDs are correct
   - Try increasing the `top_k` parameter

4. **Timeout Errors**: 
   - Increase the `ONLYSAIDKB_TIMEOUT` environment variable
   - Check network connectivity to the OnlysaidKB service

5. **Path Issues**:
   - Ensure the full path to the onlysaidkb-mcp-server directory is correct
   - Use absolute paths rather than relative paths
   - Check that the `src/onlysaidkb_mcp/main.py` file exists in the specified directory

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export ONLYSAIDKB_DEBUG=true
```

## API Compatibility

This MCP server is designed to work with the OnlysaidKB backend API. It expects the following endpoints (relative to the base URL):

- `POST /query` - Query with AI generation
- `POST /retrieve` - Document retrieval only
- `GET /view/{workspace_id}` - View workspace structure and list knowledge bases
- `GET /kb_status/{workspace_id}/{kb_id}` - Get knowledge base status

**Base URL**: `http://onlysaid-dev.com/api/kb` (includes the `/api/kb` prefix)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues related to:
- **MCP Server**: Create an issue in this repository
- **OnlysaidKB Configuration**: Check OnlysaidKB documentation
- **API Issues**: Verify OnlysaidKB service status and endpoints