"""Tool execution module for agentic planning.

Provides web search (DuckDuckGo) and text summarization (DistilBART) capabilities
with robust error handling and retry logic for reliable plan execution.
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from transformers import pipeline, Pipeline
import config


class Tools:
    """Web search and text summarization tools.
    
    Provides search_web (DuckDuckGo) and summarize_text (DistilBART)
    capabilities for agentic plan execution.
    """
    
    def __init__(self, verbose: bool = False) -> None:
        """Initialize tools with DistilBART summarization model.
        
        Args:
            verbose: Enable detailed execution logging
        """
        self.verbose: bool = verbose
        self.summarizer: Pipeline
        if self.verbose:
            print("[TOOLS] Initializing DistilBART for summarization")
            print("[MODEL] DistilBART-CNN (306M parameters, optimized for summarization)")
        
        try:
            self.summarizer = pipeline("summarization", 
                                     model=config.SUMMARIZATION_MODEL,
                                     max_length=config.SUMMARIZATION_MAX_LENGTH,
                                     min_length=config.SUMMARIZATION_MIN_LENGTH,
                                     do_sample=False)
            
            if self.verbose:
                print("[TOOLS] Summarization model loaded successfully")
        except Exception as e:
            error_msg = f"Failed to load summarization model {config.SUMMARIZATION_MODEL}: {e}"
            if self.verbose:
                print(f"[ERROR] {error_msg}")
            raise RuntimeError(error_msg)
    
    def search_web(self, query: str) -> str:
        """Search web using DuckDuckGo API with retry logic.
        
        Args:
            query: Search terms to query
            
        Returns:
            Formatted search results or error message
        """
        # Retry logic for network failures
        max_retries = config.MAX_RETRY_ATTEMPTS
        for attempt in range(max_retries):
            try:
                if self.verbose:
                    print(f"\n[SEARCH] Querying DuckDuckGo API")
                    print(f"[QUERY] '{query}'")
                    print(f"[ENDPOINT] https://api.duckduckgo.com/")
                
                url = "https://api.duckduckgo.com/"
                params = {
                    'q': query,
                    'format': 'json',
                    'no_html': '1',
                    'skip_disambig': '1'
                }
                
                if self.verbose:
                    retry_msg = f" (attempt {attempt + 1}/{max_retries})" if attempt > 0 else ""
                    print(f"[REQUEST] Sending HTTP request (timeout: 10s){retry_msg}")
                
                response = requests.get(url, params=params, timeout=config.API_TIMEOUT_SECONDS)
                response.raise_for_status()
                
                # Parse JSON response
                data = response.json()
                
                # Success - break out of retry loop
                break
                
            except (requests.RequestException, requests.Timeout, json.JSONDecodeError) as e:
                if attempt < max_retries - 1:
                    if self.verbose:
                        print(f"[RETRY] Network error, retrying in 1s: {e}")
                    time.sleep(config.RETRY_DELAY_SECONDS)
                    continue
                else:
                    # Final attempt failed
                    return f"Search failed after {max_retries} attempts: Network error"
            except Exception as e:
                return f"Search failed: {str(e)}"
        
        # Continue with successful response processing
        if self.verbose:
            print(f"[RESPONSE] HTTP {response.status_code} received")
            print(f"[PROCESSING] Parsing API response")
            print(f"[FIELDS] {len(data.keys())} response fields available")
        
        # Extract relevant information
        results = []
        
        # Get abstract first (primary content)
        if data.get('Abstract'):
            results.append(f"Abstract: {data['Abstract']}")
            if self.verbose:
                print(f"[DATA] Found abstract: {len(data['Abstract'])} chars")
        
        # Get instant answer if available (secondary)
        if data.get('Answer'):
            results.append(f"Answer: {data['Answer']}")
            if self.verbose:
                print(f"[DATA] Found instant answer: {len(data['Answer'])} chars")
        
        # Get related topics
        if data.get('RelatedTopics'):
            topic_count = len(data['RelatedTopics'])
            if self.verbose:
                print(f"[DATA] Found {topic_count} related topics (showing first 3)")
            for topic in data['RelatedTopics'][:3]:  # Limit to first 3
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append(f"Related: {topic['Text']}")
        
        if not results:
            if self.verbose:
                print(f"[WARNING] No structured data found in API response")
            return f"No detailed results found for '{query}'"
        
        final_result = "\n".join(results)
        if self.verbose:
            print(f"[COMPLETE] Search finished: {len(results)} sections, {len(final_result)} chars")
        
        return final_result
    
    def summarize_text(self, text: str) -> str:
        """Summarize text using DistilBART model.
        
        Args:
            text: Input text to summarize
            
        Returns:
            Concise summary or error message
        """
        try:
            if not text.strip():
                return "No text provided to summarize"
            
            if self.verbose:
                print(f"\n[SUMMARIZE] Processing text with DistilBART")
                print(f"[INPUT] Length: {len(text)} characters")
            
            # Truncate text if too long for the model (DistilBART can handle ~1024 tokens)
            max_input_length = 800
            original_length = len(text)
            if len(text) > max_input_length:
                text = text[:max_input_length] + "..."
                if self.verbose:
                    print(f"[TRUNCATE] Reduced from {original_length} to {len(text)} chars")
            
            if self.verbose:
                print(f"[INFERENCE] Running DistilBART (max_length=100, min_length=30)")
            
            # Use the summarization pipeline
            summary_result = self.summarizer(text, max_length=config.SUMMARIZATION_MAX_LENGTH, min_length=config.SUMMARIZATION_MIN_LENGTH, do_sample=False)
            
            if summary_result and isinstance(summary_result, list) and len(summary_result) > 0:
                summary = summary_result[0]['summary_text']
                if self.verbose:
                    print(f"[OUTPUT] Summary generated: {len(summary)} characters")
                    print(f"[METRICS] Compression ratio: {len(summary)/len(text):.2f} (lower = more compressed)")
                return summary
            else:
                if self.verbose:
                    print(f"[WARNING] No summary generated by model")
                return "Summary could not be generated"
            
        except Exception as e:
            if self.verbose:
                print(f"[ERROR] Summarization failed: {str(e)}")
            return f"Summarization failed: {str(e)}"
    
    def execute_tool(self, tool_name: str, argument: str) -> str:
        """Execute specified tool with given argument.
        
        Args:
            tool_name: Name of tool to execute (search_web, summarize_text)
            argument: Argument to pass to the tool
            
        Returns:
            Tool execution result or error message
        """
        if tool_name == "search_web":
            return self.search_web(argument)
        elif tool_name == "summarize_text":
            return self.summarize_text(argument)
        else:
            return f"Unknown tool: {tool_name}"