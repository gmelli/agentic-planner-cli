import json
import re
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, Pipeline
from logger import AgenticLogger
import config


class Planner:
    """AI-powered goal decomposition using Flan-T5-Small.
    
    Converts natural language goals into executable step sequences
    using an instruction-tuned language model.
    """
    
    def __init__(self, verbose: bool = False, explain: bool = False) -> None:
        """Initialize the planner with Flan-T5-Small model.
        
        Args:
            verbose: Enable detailed execution logging
            explain: Show AI reasoning process to user
        """
        self.verbose: bool = verbose
        self.explain: bool = explain
        self.logger: AgenticLogger = AgenticLogger(verbose=verbose)
        self.tokenizer: AutoTokenizer
        self.model: AutoModelForSeq2SeqLM  
        self.generator: Pipeline
        
        if self.verbose:
            print("[PLANNER] Initializing Flan-T5-Small for goal decomposition")
            print("[MODEL] Flan-T5-Small (220M parameters, instruction-tuned)")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(config.PLANNING_MODEL)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(config.PLANNING_MODEL)
            self.generator = pipeline("text2text-generation", 
                                    model=self.model, 
                                    tokenizer=self.tokenizer,
                                    max_length=config.PLANNING_MAX_LENGTH,
                                    do_sample=False)
                
            if self.verbose:
                print("[PLANNER] Model loaded successfully")
                
        except Exception as e:
            error_msg = f"Failed to load planning model {config.PLANNING_MODEL}: {e}"
            self.logger.log_error("PLANNER", error_msg)
            raise RuntimeError(error_msg)
    
    def plan(self, goal: str) -> List[Dict[str, Any]]:
        """Generate executable plan from natural language goal.
        
        Args:
            goal: Natural language description of desired outcome
            
        Returns:
            List of step dictionaries with 'tool' and 'argument' keys
        """
        if self.verbose:
            print(f"\n[PLANNING] Breaking down goal: '{goal}'")
        
        # Extract key terms from the goal for better search queries
        search_query = goal.replace("Find information about ", "").replace("Research ", "").replace("Explain ", "")
        
        if self.verbose:
            print(f"[EXTRACTION] Converted to search query: '{search_query}'")
        
        # Use instruction-tuned prompt for Flan-T5
        prompt = f"""Create a 2-step plan to achieve this goal using these tools:

Available tools:
- search_web: searches the web
- summarize_text: summarizes text

Goal: {goal}

Output format:
Step 1: search_web(search query here)
Step 2: summarize_text(search results)

Plan:"""
        
        if self.verbose:
            print(f"\n[PROMPT] Engineering instruction for Flan-T5")
            print(f"[PROMPT] Length: {len(prompt)} characters")
            print(f"[PARAMS] Max length: 150, temperature: 0.1 (deterministic)")
        
        try:
            if self.verbose:
                print("[INFERENCE] Generating plan with Flan-T5-Small")
            
            response = self.generator(prompt, max_length=80, num_return_sequences=1)
            generated_text = response[0]['generated_text']
            
            if self.verbose:
                print(f"[RESPONSE] Generated {len(generated_text)} characters")
                print(f"[RESPONSE] Full output: '{generated_text}'")
            
            if self.explain:
                print(f"\n🧠 AI REASONING:")
                print(f"📝 Original goal: '{goal}'")
                print(f"🔍 Extracted search terms: '{search_query}'")
                print(f"🤖 Flan-T5 generated: '{generated_text}'")
                print(f"⚙️  Parsing logic converted this into executable steps")
            
            # Parse the generated plan
            steps = self._parse_steps(generated_text, search_query)
            
            # Fallback to default plan if parsing fails
            if not steps:
                if self.verbose:
                    print("[FALLBACK] Using default plan structure")
                steps = [
                    {'tool': 'search_web', 'argument': search_query},
                    {'tool': 'summarize_text', 'argument': 'search results'}
                ]
            
            if self.verbose:
                print(f"\n[PLAN] Generated execution plan:")
                for i, step in enumerate(steps, 1):
                    print(f"  Step {i}: {step['tool']}('{step['argument']}')")
                print(f"[PLAN] Total steps: {len(steps)}")
            
            return steps
            
        except Exception as e:
            print(f"[ERROR] Planning failed: {e}")
            # Return fallback plan
            return [
                {'tool': 'search_web', 'argument': search_query},
                {'tool': 'summarize_text', 'argument': 'search results'}
            ]
    
    def _parse_steps(self, plan_text: str, search_query: str) -> List[Dict[str, Any]]:
        """Parse Flan-T5 output into structured step format.
        
        Args:
            plan_text: Raw model output text
            search_query: Extracted search terms for fallback
            
        Returns:
            List of parsed steps with tool names and arguments
        """
        steps = []
        lines = plan_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for tool names and handle arguments (use if/if to find both)
            if 'search_web' in line.lower():
                steps.append({
                    'tool': 'search_web',
                    'argument': search_query
                })
            if 'summarize_text' in line.lower():
                steps.append({
                    'tool': 'summarize_text', 
                    'argument': 'search results'
                })
        
        # If no valid steps found, create a default plan using the actual goal
        if not steps:
            steps = [
                {'tool': 'search_web', 'argument': search_query},
                {'tool': 'summarize_text', 'argument': 'search results'}
            ]
        
        return steps