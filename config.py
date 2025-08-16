"""Configuration constants for the Agentic Planner CLI."""

# Model Configuration - Lite vs Full profiles
MODEL_PROFILES = {
    "lite": {
        "planning": "google/flan-t5-base",  # 250M params, faster inference
        "summarization": "facebook/bart-large-cnn",  # Alternative option
        "ram_usage": "~800MB",
        "disk_usage": "~400MB"
    },
    "full": {
        "planning": "google/flan-t5-small", 
        "summarization": "sshleifer/distilbart-cnn-12-6",
        "ram_usage": "~1.5GB", 
        "disk_usage": "~550MB"
    }
}

# Default model configuration
MODEL_PROFILE = "full"
PLANNING_MODEL = MODEL_PROFILES[MODEL_PROFILE]["planning"]
SUMMARIZATION_MODEL = MODEL_PROFILES[MODEL_PROFILE]["summarization"]

# Generation Parameters
PLANNING_MAX_LENGTH = 80
SUMMARIZATION_MAX_LENGTH = 100
SUMMARIZATION_MIN_LENGTH = 30

# Network Configuration
API_TIMEOUT_SECONDS = 10
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 1

# Input Validation
MIN_GOAL_LENGTH = 5
MAX_GOAL_LENGTH = 200
DEFAULT_MAX_STEPS = 10

# Logging
DEFAULT_LOG_LEVEL = "INFO"
VERBOSE_LOG_LEVEL = "DEBUG"