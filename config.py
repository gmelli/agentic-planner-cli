"""Configuration constants for the Agentic Planner CLI."""

# Model Configuration
PLANNING_MODEL = "google/flan-t5-small"
SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"

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