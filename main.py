"""
MCP Homework Server

A Model Context Protocol (MCP) server providing tools for:
- Adding numbers
- Fetching web page content via Jina Reader
- Searching FastMCP documentation
"""

from fastmcp import FastMCP
import requests
import zipfile
from pathlib import Path
import minsearch

# Constants
REQUEST_TIMEOUT = 30  # seconds
ZIP_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_PATH = Path(__file__).parent / "fastmcp-main.zip"

mcp = FastMCP("MCP Homework")

# Global index cache
_index = None


class FetchError(Exception):
    """Raised when fetching content fails."""
    pass


class SearchError(Exception):
    """Raised when search operation fails."""
    pass


def _download_zip() -> None:
    """Download the fastmcp zip if not already downloaded.
    
    Raises:
        FetchError: If download fails.
    """
    if ZIP_PATH.exists():
        return
    try:
        response = requests.get(ZIP_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        with open(ZIP_PATH, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        raise FetchError(f"Failed to download fastmcp zip: {e}") from e


def _build_index() -> minsearch.Index:
    """Build minsearch index from md/mdx files in the zip.
    
    Returns:
        The minsearch index.
        
    Raises:
        SearchError: If indexing fails.
    """
    global _index
    if _index is not None:
        return _index
    
    try:
        _download_zip()
        
        documents = []
        with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
            for name in zf.namelist():
                if name.endswith('.md') or name.endswith('.mdx'):
                    # Remove first part of path (fastmcp-main/)
                    parts = name.split('/', 1)
                    filename = parts[1] if len(parts) > 1 else name
                    
                    if not filename:  # Skip if empty after stripping
                        continue
                        
                    content = zf.read(name).decode('utf-8', errors='ignore')
                    documents.append({
                        'filename': filename,
                        'content': content
                    })
        
        _index = minsearch.Index(
            text_fields=['content', 'filename'],
            keyword_fields=[]
        )
        _index.fit(documents)
        return _index
    except Exception as e:
        raise SearchError(f"Failed to build search index: {e}") from e


def _search(query: str, top_k: int = 5) -> list[dict]:
    """Search the index and return top_k results.
    
    Args:
        query: Search query string.
        top_k: Number of results to return.
        
    Returns:
        List of matching documents.
    """
    index = _build_index()
    return index.search(query, num_results=top_k)


def _fetch_page_content(url: str) -> str:
    """Fetch page content via Jina Reader.
    
    Args:
        url: URL to fetch.
        
    Returns:
        Page content in markdown format.
        
    Raises:
        FetchError: If fetch fails.
    """
    try:
        response = requests.get(
            f"https://r.jina.ai/{url}",
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise FetchError(f"Failed to fetch page content: {e}") from e


def _add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers.
    
    Args:
        a: First number.
        b: Second number.
        
    Returns:
        Sum of a and b.
    """
    return _add(a, b)


@mcp.tool
def fetch_page_content(url: str) -> str:
    """Fetch content of a web page using Jina reader.
    
    Args:
        url: The URL of the page to fetch.
        
    Returns:
        Page content in markdown format.
    """
    return _fetch_page_content(url)


@mcp.tool
def search(query: str) -> list[dict]:
    """Search FastMCP documentation for relevant documents.
    
    Args:
        query: The search query.
    
    Returns:
        List of up to 5 most relevant documents with filename and content.
    """
    return _search(query, top_k=5)


if __name__ == "__main__":
    mcp.run()