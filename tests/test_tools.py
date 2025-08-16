import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools import Tools


class TestTools(unittest.TestCase):
    
    def setUp(self):
        with patch('tools.pipeline') as mock_pipeline:
            mock_pipeline.return_value = Mock()
            self.tools = Tools()
    
    @patch('tools.requests.get')
    def test_search_web_success(self, mock_get):
        # Mock successful API response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'Answer': 'Test answer',
            'Abstract': 'Test abstract',
            'RelatedTopics': [
                {'Text': 'Related topic 1'},
                {'Text': 'Related topic 2'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = self.tools.search_web('test query')
        
        self.assertIn('Answer: Test answer', result)
        self.assertIn('Abstract: Test abstract', result)
        self.assertIn('Related: Related topic 1', result)
    
    @patch('tools.requests.get')
    def test_search_web_no_results(self, mock_get):
        # Mock empty API response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        result = self.tools.search_web('test query')
        
        self.assertIn('No detailed results found', result)
    
    @patch('tools.requests.get')
    def test_search_web_network_error(self, mock_get):
        # Mock network error
        mock_get.side_effect = Exception('Network error')
        
        result = self.tools.search_web('test query')
        
        self.assertIn('Search failed', result)
    
    def test_summarize_text_empty(self):
        result = self.tools.summarize_text('')
        
        self.assertEqual(result, 'No text provided to summarize')
    
    def test_summarize_text_success(self):
        # Mock the summarizer to return expected format
        self.tools.summarizer = Mock()
        self.tools.summarizer.return_value = [{'summary_text': 'This is a test summary'}]
        
        result = self.tools.summarize_text('Some long text to summarize')
        
        self.assertEqual(result, 'This is a test summary')
    
    def test_summarize_text_no_results(self):
        # Mock the summarizer to return empty results
        self.tools.summarizer = Mock()
        self.tools.summarizer.return_value = []
        
        result = self.tools.summarize_text('Some text')
        
        self.assertEqual(result, 'Summary could not be generated')
    
    def test_execute_tool_search_web(self):
        with patch.object(self.tools, 'search_web', return_value='search result'):
            result = self.tools.execute_tool('search_web', 'test query')
            self.assertEqual(result, 'search result')
    
    def test_execute_tool_summarize_text(self):
        with patch.object(self.tools, 'summarize_text', return_value='summary result'):
            result = self.tools.execute_tool('summarize_text', 'test text')
            self.assertEqual(result, 'summary result')
    
    def test_execute_tool_unknown(self):
        result = self.tools.execute_tool('unknown_tool', 'argument')
        
        self.assertEqual(result, 'Unknown tool: unknown_tool')


if __name__ == '__main__':
    unittest.main()