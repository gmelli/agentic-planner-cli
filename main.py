#!/usr/bin/env python3
import argparse
import sys
import time
from typing import Dict, Any, List
from planner import Planner
from tools import Tools
from logger import AgenticLogger
import config


class Executor:
    """Executes planned steps using available tools.
    
    Manages step-by-step execution with context passing,
    timing metrics, and result aggregation.
    """
    
    def __init__(self, max_steps: int = config.DEFAULT_MAX_STEPS, verbose: bool = False) -> None:
        """Initialize executor with configuration.
        
        Args:
            max_steps: Maximum number of steps to execute
            verbose: Enable detailed execution logging
        """
        self.max_steps: int = max_steps
        self.verbose: bool = verbose
        self.context: Dict[str, Any] = {}
        self.logger: AgenticLogger = AgenticLogger(verbose=verbose)
        self.tools: Tools
        
        if self.verbose:
            print("[EXECUTOR] Initializing agentic execution engine")
            print(f"[CONFIG] max_steps={max_steps}, verbose={verbose}")
        
        self.tools = Tools(verbose=verbose)
    
    def execute_plan(self, steps: List[Dict[str, Any]], goal: str) -> str:
        """Execute sequence of planned steps.
        
        Args:
            steps: List of step dictionaries with tool and argument
            goal: Original user goal for context
            
        Returns:
            Final execution result (single or concatenated)
        """
        if self.verbose:
            print(f"\n[EXECUTION] Starting agentic plan execution")
            print(f"[GOAL] {goal}")
            print(f"[PLAN] {len(steps)} steps to execute")
            print(f"[LIMIT] Maximum {self.max_steps} steps allowed")
        
        results = []
        
        for i, step in enumerate(steps[:self.max_steps]):
            if self.verbose:
                print(f"\n{'='*50}")
                print(f"[STEP {i+1}/{len(steps)}] {step['tool']}('{step['argument']}')")
            
            # Execute the tool, substituting context if needed
            argument = step['argument']
            if argument == 'search results' and 'last_search_result' in self.context:
                if self.verbose:
                    print(f"[CONTEXT] Substituting with previous search results ({len(self.context['last_search_result'])} chars)")
                argument = self.context['last_search_result']
            
            if self.verbose:
                print(f"[EXECUTE] {step['tool']} with input: {len(argument)} chars")
            
            # Execute with timing
            start_time = time.time()
            result = self.tools.execute_tool(step['tool'], argument)
            duration_ms = (time.time() - start_time) * 1000
            
            # Handle None results
            if result is None:
                result = f"Tool {step['tool']} returned no result"
            
            # Log execution
            self.logger.log_tool_execution(i+1, step['tool'], argument, len(result), duration_ms)
            
            if self.verbose:
                print(f"[RESULT] Step {i+1} complete: {len(result)} chars output")
                print(f"[PREVIEW] {result[:120]}{'...' if len(result) > 120 else ''}")
            
            results.append(result)
            
            # Store result in context for potential use by next steps
            self.context[f"step_{i+1}_result"] = result
            
            # If this was a search, make the result available for summarization
            if step['tool'] == 'search_web':
                self.context['last_search_result'] = result
                if self.verbose:
                    print(f"[CONTEXT] Search results stored for next step")
        
        if self.verbose:
            print(f"\n[COMPLETE] All {len(results)} steps executed")
            print(f"[SUMMARY] Total output: {sum(len(r) for r in results)} characters")
        
        # Return the final result or concatenated results
        if len(results) == 1:
            return results[0]
        else:
            return "\n\n".join(f"Step {i+1} result:\n{result}" for i, result in enumerate(results))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agentic Planner CLI - Break down goals into actionable steps",
        epilog="""
GOOD EXAMPLES:
  "Find information about quantum computing"
  "Research artificial intelligence trends"
  "Explain machine learning basics"

AVOID THESE:
  "Calculate 2+2" (math problems)
  "Write Python code" (code generation)
  "Debug my program" (technical tasks)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("goal", help="The goal you want to achieve")
    parser.add_argument("--max-steps", type=int, default=config.DEFAULT_MAX_STEPS, help="Maximum number of steps to execute")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--explain", action="store_true", help="Show how the AI decomposes the goal")
    
    args = parser.parse_args()
    
    # Input validation
    goal = args.goal.strip()
    if not goal:
        print("❌ ERROR: Goal cannot be empty")
        print("💡 HELP: Provide a clear goal like 'Research machine learning' or 'Explain Docker containers'")
        sys.exit(1)
    
    if len(goal) < config.MIN_GOAL_LENGTH:
        print(f"❌ ERROR: Goal too short (minimum {config.MIN_GOAL_LENGTH} characters)")
        print("💡 HELP: Provide a more descriptive goal")
        sys.exit(1)
    
    if len(goal) > config.MAX_GOAL_LENGTH:
        print(f"❌ ERROR: Goal too long (maximum {config.MAX_GOAL_LENGTH} characters)")
        print("💡 HELP: Simplify your goal or break it into smaller parts")
        sys.exit(1)
    
    # Filter potentially problematic characters
    if any(char in goal for char in ['<', '>', '&', '|', ';', '`']):
        print("❌ ERROR: Goal contains invalid characters")
        print("💡 HELP: Use only letters, numbers, spaces, and basic punctuation")
        sys.exit(1)
    
    # Detect non-searchable goals
    math_patterns = ['calculate', 'compute', 'solve', '=', '+', '-', '*', '/', 'math']
    code_patterns = ['write code', 'write python', 'write java', 'implement', 'debug', 'fix bug', 'program']
    
    if any(pattern in goal.lower() for pattern in math_patterns):
        print("❌ ERROR: This tool searches and summarizes web content")
        print("💡 HELP: Try goals like 'Find information about X' or 'Research Y topic'")
        sys.exit(1)
    
    if any(pattern in goal.lower() for pattern in code_patterns):
        print("❌ ERROR: This tool demonstrates planning, not code generation")
        print("💡 HELP: Try research goals like 'Explain machine learning' or 'Find news about AI'")
        sys.exit(1)
    
    try:
        # Initialize planner and executor
        if args.verbose:
            print("AGENTIC PLANNER CLI - Technical Demonstration")
            print("=" * 50)
            print("Demonstrates AI-driven goal decomposition and execution")
            print("Architecture: Goal → Plan (Flan-T5-Small) → Execute (Search + Summarize)")
            print("=" * 50)
        
        planner = Planner(verbose=args.verbose, explain=args.explain)
        executor = Executor(max_steps=args.max_steps, verbose=args.verbose)
        
        # Generate plan with timing
        plan_start = time.time()
        steps = planner.plan(goal)
        plan_duration = (time.time() - plan_start) * 1000
        
        if not steps:
            print("❌ ERROR: Could not generate a valid plan")
            sys.exit(1)
        
        # Execute plan with timing
        exec_start = time.time()
        result = executor.execute_plan(steps, goal)
        exec_duration = (time.time() - exec_start) * 1000
        
        # Output final result with timing
        total_duration = plan_duration + exec_duration
        
        if args.verbose or args.explain:
            print(f"\n⏱️  PERFORMANCE BREAKDOWN:")
            print(f"   Planning: {plan_duration:.1f}ms ({plan_duration/total_duration*100:.1f}%)")
            print(f"   Execution: {exec_duration:.1f}ms ({exec_duration/total_duration*100:.1f}%)")
            print(f"   Total: {total_duration:.1f}ms")
        
        if args.verbose:
            print("\n" + "="*50)
            print("FINAL RESULT - Agentic Planning Complete")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("FINAL RESULT:")
            print("="*50)
        print(result)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()