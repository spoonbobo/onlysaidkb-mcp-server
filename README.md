# OnlysaidKB MCP Server

A Model Context Protocol (MCP) server for OnlysaidKB (Knowledge Base) integration. This server provides tools for querying and retrieving information from knowledge bases using natural language.

## Features

### 🔧 MCP Tools

1. **`query_knowledge_base`** - Query knowledge bases with AI-generated answers
   - Performs both document retrieval and AI generation
   - Supports conversation history for context
   - Customizable model, top-k, and language settings

2. **`retrieve_from_knowledge_base`** - Pure document retrieval without AI generation
   - Returns raw documents with similarity scores
   - Useful for getting source material or custom processing

### 📚 MCP Resources

1. **`onlysaidkb://workspace/{workspace_id}/knowledge_bases`** - List all knowledge bases in a workspace
2. **`onlysaidkb://workspace/{workspace_id}/kb/{kb_id}/status`** - Get knowledge base status
3. **`onlysaidkb://workspace/{workspace_id}/structure`** - View workspace structure

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd onlysaidkb-mcp-server

# Install dependencies with uv
uv sync

# Or install for development
uv sync --dev
```

### Using pip

```bash
pip install -e .

# Or for development
pip install -e ".[dev]"
```

## Configuration

Set the following environment variables:

### Required
- `ONLYSAIDKB_BASE_URL` - Base URL of your OnlysaidKB API (e.g., `http://localhost:8000`)

### Optional
- `ONLYSAIDKB_DEFAULT_MODEL` - Default AI model to use (default: `gpt-4`)
- `ONLYSAIDKB_DEFAULT_TOP_K` - Default number of documents to retrieve (default: `5`)
- `ONLYSAIDKB_DEFAULT_LANGUAGE` - Default response language (default: `en`)
- `ONLYSAIDKB_TIMEOUT` - Request timeout in seconds (default: `30`)

### Example Configuration

```bash
export ONLYSAIDKB_BASE_URL="http://localhost:8000"
export ONLYSAIDKB_DEFAULT_MODEL="gpt-4"
export ONLYSAIDKB_DEFAULT_TOP_K="5"
export ONLYSAIDKB_DEFAULT_LANGUAGE="en"
```

## Usage

### Running the Server

```bash
# Using the installed script
onlysaidkb-mcp-server

# Or directly with Python
python -m onlysaidkb_mcp.main

# Or from source
python src/onlysaidkb_mcp/main.py
```

### MCP Tool Usage Examples

#### Query Knowledge Base
```python
# Basic query
result = await query_knowledge_base(
    workspace_id="my-workspace",
    query="What is the main purpose of this system?"
)

# Query with specific knowledge bases
result = await query_knowledge_base(
    workspace_id="my-workspace",
    query="How do I configure authentication?",
    knowledge_bases=["kb-1", "kb-2"],
    top_k=3
)

# Query with conversation history
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

#### Retrieve Documents
```python
# Basic retrieval
result = await retrieve_from_knowledge_base(
    workspace_id="my-workspace",
    query="system configuration",
    top_k=10
)

# Retrieval from specific knowledge bases
result = await retrieve_from_knowledge_base(
    workspace_id="my-workspace",
    query="API documentation",
    knowledge_bases=["docs-kb", "api-kb"]
)
```

## API Compatibility

This MCP server is designed to work with the OnlysaidKB backend API. It expects the following endpoints:

- `POST /query` - Query with AI generation
- `POST /retrieve` - Document retrieval only
- `GET /list_documents/{workspace_id}` - List knowledge bases
- `GET /kb_status/{workspace_id}/{kb_id}` - Get KB status
- `GET /view/{workspace_id}` - View workspace structure

## Testing

### Run All Tests

```bash
# Install test dependencies
uv sync --dev

# Run connectivity tests
python tests/connectivity_test.py

# Run API tests
python tests/test_onlysaidkb_api.py

# Run MCP tools tests
python tests/mcp_tools_test.py
```

### Test Configuration

Set these environment variables for testing:

```bash
export ONLYSAIDKB_BASE_URL="http://localhost:8000"
export TEST_WORKSPACE_ID="your-test-workspace-id"
export TEST_KB_IDS="kb-1,kb-2,kb-3"
```

### Test Categories

1. **Connectivity Tests** (`connectivity_test.py`)
   - Basic server connectivity
   - Health checks
   - API availability

2. **API Tests** (`test_onlysaidkb_api.py`)
   - Complete API functionality testing
   - Query and retrieval operations
   - Error handling scenarios

3. **MCP Tools Tests** (`mcp_tools_test.py`)
   - Direct MCP tool function testing
   - Resource testing
   - Tool parameter validation

## Development

### Project Structure

```
onlysaidkb-mcp-server/
├── src/onlysaidkb_mcp/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   └── server.py        # MCP server implementation
├── tests/
│   ├── connectivity_test.py
│   ├── test_onlysaidkb_api.py
│   └── mcp_tools_test.py
├── pyproject.toml
└── README.md
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest --cov=src tests/
```

## Comparison with TypeScript Service

This MCP server replicates the functionality of the TypeScript `onlysaid_kb.ts` service:

| TypeScript Method | MCP Tool/Resource | Description |
|-------------------|-------------------|-------------|
| `queryKnowledgeBase()` | `query_knowledge_base` | AI-powered query with generation |
| `queryKnowledgeBaseNonStreaming()` | `query_knowledge_base` (streaming=false) | Non-streaming queries |
| `retrieveFromKnowledgeBase()` | `retrieve_from_knowledge_base` | Document retrieval only |
| `listKnowledgeBases()` | Resource: `knowledge_bases` | List workspace KBs |
| `getKnowledgeBaseStatus()` | Resource: `kb/{kb_id}/status` | Get KB status |
| `viewKnowledgeBaseStructure()` | Resource: `structure` | View workspace structure |

## Error Handling

The server provides comprehensive error handling:

- **HTTP Errors**: Captured and returned with status codes
- **Connection Errors**: Handled gracefully with descriptive messages
- **Invalid Parameters**: Validated and reported clearly
- **Debug Information**: Included in responses for troubleshooting

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## Support

For issues and questions:
- Check the test files for usage examples
- Review the debug information in tool responses
- Ensure your OnlysaidKB backend is running and accessible