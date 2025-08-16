import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from planner import Planner


class TestPlanner(unittest.TestCase):
    
    @patch('planner.pipeline')
    @patch('planner.AutoModelForSeq2SeqLM')
    @patch('planner.AutoTokenizer')
    def setUp(self, mock_tokenizer, mock_model, mock_pipeline):
        # Mock the tokenizer
        mock_tokenizer_instance = Mock()
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        
        # Mock the model
        mock_model_instance = Mock()
        mock_model.from_pretrained.return_value = mock_model_instance
        
        # Mock the pipeline
        mock_pipeline_instance = Mock()
        mock_pipeline.return_value = mock_pipeline_instance
        
        self.planner = Planner()
        self.mock_generator = mock_pipeline_instance
    
    def test_parse_steps_valid_format(self):
        plan_text = """
        Step 1: search_web(quantum computing news)
        Step 2: summarize_text(search results)
        """
        
        steps = self.planner._parse_steps(plan_text, "quantum computing")
        
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]['tool'], 'search_web')
        self.assertEqual(steps[0]['argument'], 'quantum computing')  # Uses search_query param
        self.assertEqual(steps[1]['tool'], 'summarize_text')
        self.assertEqual(steps[1]['argument'], 'search results')
    
    def test_parse_steps_invalid_tools_filtered(self):
        plan_text = """
        Step 1: search_web(valid query)
        Step 2: invalid_tool(some argument)
        Step 3: summarize_text(valid text)
        """
        
        steps = self.planner._parse_steps(plan_text, "test query")
        
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]['tool'], 'search_web')
        self.assertEqual(steps[0]['argument'], 'test query')  # Uses search_query param
        self.assertEqual(steps[1]['tool'], 'summarize_text')
        self.assertEqual(steps[1]['argument'], 'search results')
    
    def test_parse_steps_empty_returns_default(self):
        plan_text = ""
        
        steps = self.planner._parse_steps(plan_text, "test query")
        
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]['tool'], 'search_web')
        self.assertEqual(steps[0]['argument'], 'test query')  # Uses search_query param
        self.assertEqual(steps[1]['tool'], 'summarize_text')
        self.assertEqual(steps[1]['argument'], 'search results')
    
    def test_plan_with_mock_response(self):
        mock_response = [{
            'generated_text': "Step 1: search_web(AI news)\nStep 2: summarize_text(search results)"
        }]
        
        self.mock_generator.return_value = mock_response
        
        steps = self.planner.plan("Find news about AI")
        
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]['tool'], 'search_web')
        self.assertEqual(steps[0]['argument'], 'Find news about AI')  # Uses extracted search_query


if __name__ == '__main__':
    unittest.main()