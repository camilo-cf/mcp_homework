"""Tests for MCP Homework tools."""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import _add, _fetch_page_content, _search, FetchError


class TestAdd:
    """Tests for the add function."""
    
    def test_add_positive_numbers(self):
        assert _add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        assert _add(-1, -2) == -3
    
    def test_add_zero(self):
        assert _add(0, 5) == 5
    
    def test_add_large_numbers(self):
        assert _add(1000000, 2000000) == 3000000


class TestFetchPageContent:
    """Tests for the fetch_page_content function."""
    
    @patch('main.requests.get')
    def test_fetch_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "# Test Content"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        result = _fetch_page_content("https://example.com")
        
        assert result == "# Test Content"
        mock_get.assert_called_once()
    
    @patch('main.requests.get')
    def test_fetch_timeout(self, mock_get):
        import requests
        mock_get.side_effect = requests.Timeout("Connection timed out")
        
        with pytest.raises(FetchError):
            _fetch_page_content("https://example.com")


class TestSearch:
    """Tests for the search function."""
    
    @patch('main._build_index')
    def test_search_returns_results(self, mock_build_index):
        mock_index = MagicMock()
        mock_index.search.return_value = [
            {'filename': 'test.md', 'content': 'test content'}
        ]
        mock_build_index.return_value = mock_index
        
        results = _search("test", top_k=5)
        
        assert len(results) == 1
        assert results[0]['filename'] == 'test.md'
    
    @patch('main._build_index')
    def test_search_empty_query(self, mock_build_index):
        mock_index = MagicMock()
        mock_index.search.return_value = []
        mock_build_index.return_value = mock_index
        
        results = _search("", top_k=5)
        
        assert results == []
