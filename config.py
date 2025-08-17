"""Configuration constants for the Agentic Planner CLI."""

# Model Configuration - Use same models with different resource profiles
# Both profiles use flan-t5-small (80M) + distilbart-cnn (306M) = 386M total
PLANNING_MODEL = "google/flan-t5-small"
SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"

# Profile differences are in inference configuration, not model choice
MODEL_PROFILES = {
    "lite": {
        "description": "Lower memory usage, faster inference",
        "ram_usage": "~1.2GB",
        "disk_usage": "~450MB"
    },
    "full": {
        "description": "Standard configuration",
        "ram_usage": "~1.5GB", 
        "disk_usage": "~550MB"
    }
}

# Default profile
MODEL_PROFILE = "full"

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