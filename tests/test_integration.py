"""Integration tests for Agentic Planner CLI.

These tests make real API calls and test the complete Docker workflow.
Run sparingly to avoid rate limiting.
"""

import unittest
import subprocess
import json
import requests
import time
from typing import Dict, Any


class TestDuckDuckGoIntegration(unittest.TestCase):
    """Test real DuckDuckGo API responses."""
    
    def setUp(self):
        self.api_url = "https://api.duckduckgo.com/"
        self.timeout = 10
    
    def test_api_quantum_computing_response(self):
        """Test quantum computing query returns Abstract field."""
        params = {
            'q': 'quantum computing',
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        response = requests.get(self.api_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        # Should have Abstract but not Answer for this query
        self.assertTrue(data.get('Abstract'), "Should have Abstract field")
        self.assertGreater(len(data.get('Abstract', '')), 100, "Abstract should be substantial")
        self.assertFalse(data.get('Answer'), "Should not have Answer for this query")
    
    def test_api_machine_learning_response(self):
        """Test machine learning query structure."""
        params = {
            'q': 'machine learning',
            'format': 'json', 
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        response = requests.get(self.api_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        # Verify expected fields
        self.assertIn('Abstract', data)
        self.assertIn('RelatedTopics', data)
        self.assertIsInstance(data['RelatedTopics'], list)
        
        # Abstract should be substantial for ML topic
        abstract = data.get('Abstract', '')
        self.assertGreater(len(abstract), 200, "ML abstract should be detailed")
        self.assertIn('artificial intelligence', abstract.lower())
    
    def test_api_empty_query_handling(self):
        """Test how API handles empty or invalid queries."""
        params = {
            'q': '',
            'format': 'json',
            'no_html': '1', 
            'skip_disambig': '1'
        }
        
        response = requests.get(self.api_url, params=params, timeout=self.timeout)
        # Should not raise exception, API handles gracefully
        response.raise_for_status()
        
        # DuckDuckGo returns empty response for empty query, handle gracefully
        try:
            data = response.json()
            # Empty query should return minimal data
            self.assertFalse(data.get('Abstract'))
            self.assertFalse(data.get('Answer'))
        except requests.exceptions.JSONDecodeError:
            # API returns empty response for empty query - this is expected
            self.assertTrue(True, "Empty query correctly returns empty response")


class TestDockerIntegration(unittest.TestCase):
    """Test complete Docker workflow integration."""
    
    @classmethod
    def setUpClass(cls):
        """Build Docker image once for all tests."""
        print("\nBuilding Docker image for integration tests...")
        result = subprocess.run(['docker', 'build', '-t', 'agentic-planner-cli', '.'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode != 0:
            raise RuntimeError(f"Docker build failed: {result.stderr}")
        print("Docker image built successfully")
    
    def run_docker_command(self, goal: str, extra_args: list = None) -> Dict[str, Any]:
        """Helper to run Docker command and parse output."""
        cmd = ['docker', 'run', '--rm', 'agentic-planner-cli', goal]
        if extra_args:
            cmd.extend(extra_args)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
    
    def test_quantum_computing_end_to_end(self):
        """Test quantum computing query through complete pipeline."""
        result = self.run_docker_command("quantum computing")
        
        self.assertTrue(result['success'], f"Command failed: {result['stderr']}")
        self.assertIn('Abstract:', result['stdout'])
        self.assertIn('quantum computer', result['stdout'].lower())
        self.assertIn('Step 1 result:', result['stdout'])
        self.assertIn('Step 2 result:', result['stdout'])
    
    def test_machine_learning_with_explain(self):
        """Test machine learning with explain mode."""
        result = self.run_docker_command("machine learning", ["--explain"])
        
        self.assertTrue(result['success'], f"Command failed: {result['stderr']}")
        self.assertIn('[REASONING] AI Planning Process:', result['stdout'])
        self.assertIn('[GOAL] Original goal:', result['stdout'])
        self.assertIn('[PERFORMANCE] Execution Breakdown:', result['stdout'])
        self.assertIn('machine learning', result['stdout'].lower())
    
    def test_help_command(self):
        """Test help command functionality."""
        result = self.run_docker_command("--help")
        
        self.assertTrue(result['success'], f"Help failed: {result['stderr']}")
        self.assertIn('usage:', result['stdout'])
        self.assertIn('--verbose', result['stdout'])
        self.assertIn('--explain', result['stdout'])
        self.assertIn('--model-profile', result['stdout'])
    
    def test_empty_goal_validation(self):
        """Test empty goal input validation."""
        result = self.run_docker_command("")
        
        self.assertFalse(result['success'], "Empty goal should fail")
        self.assertIn('ERROR: Goal cannot be empty', result['stdout'])
    
    def test_lite_model_profile(self):
        """Test lite model profile option."""
        result = self.run_docker_command("artificial intelligence", ["--model-profile", "lite"])
        
        self.assertTrue(result['success'], f"Lite profile failed: {result['stderr']}")
        self.assertIn('Abstract:', result['stdout'])
        self.assertIn('artificial intelligence', result['stdout'].lower())
    
    def test_readme_examples_work(self):
        """Test that README examples actually work."""
        readme_examples = [
            "explain quantum computing to me",
            "help me understand machine learning", 
            "what should I know about blockchain"
        ]
        
        for example in readme_examples:
            with self.subTest(example=example):
                result = self.run_docker_command(example)
                self.assertTrue(result['success'], 
                              f"README example '{example}' failed: {result['stderr']}")
                self.assertIn('Abstract:', result['stdout'])
                self.assertNotIn('No detailed results found', result['stdout'])


class TestPerformanceIntegration(unittest.TestCase):
    """Test performance characteristics under real conditions."""
    
    def test_response_time_acceptable(self):
        """Test that typical queries complete within reasonable time."""
        start_time = time.time()
        
        result = subprocess.run(['docker', 'run', '--rm', 'agentic-planner-cli', 'neural networks'], 
                              capture_output=True, text=True, timeout=30)
        
        duration = time.time() - start_time
        
        self.assertTrue(result.returncode == 0, f"Command failed: {result.stderr}")
        self.assertLess(duration, 20, f"Query took too long: {duration:.1f}s")
        self.assertIn('Abstract:', result.stdout)


if __name__ == '__main__':
    # Run with warnings about rate limiting
    print("WARNING: Integration tests make real API calls")
    print("Run sparingly to avoid DuckDuckGo rate limiting")
    print("=" * 50)
    
    unittest.main(verbosity=2)