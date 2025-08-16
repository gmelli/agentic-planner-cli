import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import Executor


class TestExecutor(unittest.TestCase):
    
    def setUp(self):
        with patch('main.Tools'):
            self.executor = Executor(max_steps=5, verbose=False)
    
    def test_execute_plan_single_step(self):
        steps = [{'tool': 'search_web', 'argument': 'test query'}]
        
        with patch.object(self.executor.tools, 'execute_tool', return_value='search result'):
            result = self.executor.execute_plan(steps, 'test goal')
            
            self.assertEqual(result, 'search result')
    
    def test_execute_plan_multiple_steps(self):
        steps = [
            {'tool': 'search_web', 'argument': 'test query'},
            {'tool': 'summarize_text', 'argument': 'test text'}
        ]
        
        with patch.object(self.executor.tools, 'execute_tool', side_effect=['search result', 'summary result']):
            result = self.executor.execute_plan(steps, 'test goal')
            
            self.assertIn('Step 1 result:\nsearch result', result)
            self.assertIn('Step 2 result:\nsummary result', result)
    
    def test_execute_plan_respects_max_steps(self):
        steps = [
            {'tool': 'search_web', 'argument': 'query1'},
            {'tool': 'search_web', 'argument': 'query2'},
            {'tool': 'search_web', 'argument': 'query3'}
        ]
        
        with patch('main.Tools'):
            executor = Executor(max_steps=2, verbose=False)
            with patch.object(executor.tools, 'execute_tool', return_value='result'):
                result = executor.execute_plan(steps, 'test goal')
                
                # Should only execute 2 steps
                self.assertEqual(result.count('Step'), 2)
    
    def test_context_storage(self):
        steps = [{'tool': 'search_web', 'argument': 'test query'}]
        
        with patch.object(self.executor.tools, 'execute_tool', return_value='search result'):
            self.executor.execute_plan(steps, 'test goal')
            
            self.assertEqual(self.executor.context['step_1_result'], 'search result')
            self.assertEqual(self.executor.context['last_search_result'], 'search result')


if __name__ == '__main__':
    unittest.main()