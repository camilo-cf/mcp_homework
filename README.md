# MCP Homework

A Model Context Protocol (MCP) server built with [FastMCP](https://github.com/jlowin/fastmcp).

## Features

- **`add(a, b)`** - Add two numbers
- **`fetch_page_content(url)`** - Fetch web page content in markdown via [Jina Reader](https://jina.ai/)
- **`search(query)`** - Search FastMCP documentation (returns top 5 results)

## Installation

```bash
# Install dependencies
uv sync

# Install with dev dependencies (for testing)
uv sync --extra dev
```

## Usage

```bash
uv run main.py
```

## Testing

```bash
uv run pytest tests/ -v
```

## Project Structure

```
├── main.py           # MCP server implementation
├── tests/
│   └── test_main.py  # Unit tests
├── pyproject.toml    # Project configuration
└── README.md
```

## Security

- All HTTP requests use timeouts (30s default)
- Proper error handling with custom exceptions
- Input validation on all tool functions
