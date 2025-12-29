from fastmcp import FastMCP
import requests
import zipfile
import os
from pathlib import Path
from io import BytesIO
import minsearch

mcp = FastMCP("Demo 🚀")

# Global index
_index = None

ZIP_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_PATH = Path(__file__).parent / "fastmcp-main.zip"

def _download_zip():
    """Download the fastmcp zip if not already downloaded."""
    if ZIP_PATH.exists():
        return
    response = requests.get(ZIP_URL)
    response.raise_for_status()
    with open(ZIP_PATH, 'wb') as f:
        f.write(response.content)

def _build_index():
    """Build minsearch index from md/mdx files in the zip."""
    global _index
    if _index is not None:
        return _index
    
    _download_zip()
    
    documents = []
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        for name in zf.namelist():
            if name.endswith('.md') or name.endswith('.mdx'):
                # Remove first part of path (fastmcp-main/)
                parts = name.split('/', 1)
                if len(parts) > 1:
                    filename = parts[1]
                else:
                    filename = name
                
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

def _search(query: str, top_k: int = 5):
    """Search the index and return top_k results."""
    index = _build_index()
    results = index.search(query, num_results=top_k)
    return results

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def _fetch_page_content(url: str) -> str:
    response = requests.get(f"https://r.jina.ai/{url}")
    return response.text

@mcp.tool
def fetch_page_content(url: str) -> str:
    """Fetch content of a web page using Jina reader.
    
    Args:
        url: The URL of the page to fetch.
    """
    return _fetch_page_content(url)

@mcp.tool
def search(query: str) -> list[dict]:
    """Search fastmcp documentation for relevant documents.
    
    Args:
        query: The search query.
    
    Returns:
        List of up to 5 most relevant documents with filename and content.
    """
    return _search(query, top_k=5)

if __name__ == "__main__":
    mcp.run()