# MCP Homework

A Model Context Protocol (MCP) server built with [FastMCP](https://github.com/jlowin/fastmcp).

## Tools

### `add(a, b)`
Add two numbers.

### `fetch_page_content(url)`
Fetch content of a web page in markdown format using [Jina Reader](https://jina.ai/).

### `search(query)`
Search FastMCP documentation for relevant documents. Returns the 5 most relevant results.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run main.py
```

## Testing

```bash
# Test page fetching
cd tests && uv run test.py

# Test search
cd tests && uv run search.py
```
