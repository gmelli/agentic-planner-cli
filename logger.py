"""Logging utilities for agentic planning execution.

Provides structured logging for tool execution timing, performance metrics,
and debug information throughout the agentic planning workflow.
"""

import logging
import sys
from datetime import datetime
from typing import Dict, Any


class AgenticLogger:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.setup_logging()
    
    def setup_logging(self):
        # Create logger
        self.logger = logging.getLogger('agentic_planner')
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(handler)
    
    def log_planning_start(self, goal: str):
        self.logger.info(f"Planning started for goal: '{goal}'")
    
    def log_planning_complete(self, steps: list, duration_ms: float):
        self.logger.info(f"Planning complete: {len(steps)} steps in {duration_ms:.1f}ms")
    
    def log_tool_execution(self, step_id: int, tool: str, argument: str, result_size: int, duration_ms: float):
        self.logger.info(f"Step {step_id}: {tool} executed in {duration_ms:.1f}ms, output: {result_size} chars")
        if self.verbose:
            self.logger.debug(f"Step {step_id} argument: '{argument[:100]}{'...' if len(argument) > 100 else ''}'")
    
    def log_error(self, component: str, error: str, context: Dict[str, Any] = None):
        self.logger.error(f"{component} error: {error}")
        if self.verbose and context:
            self.logger.debug(f"Error context: {context}")
    
    def log_performance(self, metric: str, value: float, unit: str = ""):
        self.logger.info(f"Performance - {metric}: {value:.2f}{unit}")
    
    def log_model_load(self, model_name: str, params: str, duration_ms: float):
        self.logger.info(f"Model loaded: {model_name} ({params}) in {duration_ms:.1f}ms")