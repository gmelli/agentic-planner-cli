# Agentic Planner CLI

A lightweight command-line tool that demonstrates agentic planning using a local language model. The tool takes a user's goal, breaks it into sub-tasks using Flan-T5-Small, and executes built-in functions to achieve the goal.

## Features

- **Local Models**: Uses Flan-T5-Small for planning and DistilBART for summarization (no external API keys required)
- **Built-in Tools**: Web search via DuckDuckGo and text summarization
- **Docker Support**: Runs in a single container for easy setup
- **Agentic Loop**: Automatically plans and executes multi-step tasks

## Quick Start

### Prerequisites

- Docker installed on your system
- **Minimum 2GB RAM** (4GB recommended)
- **1GB free disk space** for model weights and container

### Build and Run

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd agentic-planner-cli
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t agentic-planner-cli .
   ```

3. **Run the tool**:
   ```bash
   docker run --rm agentic-planner-cli "Summarize two recent articles about edge computing"
   ```

## Usage Examples

```bash
# Search and summarize news
docker run --rm agentic-planner-cli "Find and summarize the latest news about quantum computing"

# Research a topic
docker run --rm agentic-planner-cli "Research artificial intelligence trends in 2024"

# Verbose output to see planning steps
docker run --rm agentic-planner-cli "Explain machine learning basics" --verbose

# Limit number of execution steps
docker run --rm agentic-planner-cli "Research climate change solutions" --max-steps 3
```

## Command Line Options

- `goal`: The goal you want to achieve (required)
- `--max-steps N`: Maximum number of steps to execute (default: 10)
- `--verbose, -v`: Enable verbose output showing planning and execution details

## Available Tools

The planner can use these built-in tools:

- **search_web(query)**: Searches the web using DuckDuckGo API
- **summarize_text(text)**: Generates a concise summary using DistilBART

## Development

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   python -m pytest tests/ -v
   ```

3. Run locally:
   ```bash
   python main.py "your goal here" --verbose
   ```

### Testing

The project includes comprehensive unit tests that mock external dependencies:

```bash
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

## Resource Requirements

### System Requirements
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: Any modern x86_64 or ARM64 processor
- **Disk**: 1GB free space (500MB for models + 500MB for container)
- **Network**: Internet connection for initial model download and web search

### Model Details
- **Flan-T5-Small**: 220M parameters, ~300MB download (planning)
- **DistilBART-CNN**: 306M parameters, ~250MB download (summarization)
- **Total**: 526M parameters, ~550MB disk usage

### Performance Expectations
- **First run**: 2-4 minutes (model downloads)
- **Subsequent runs**: 10-30 seconds per query
- **Memory usage**: ~1.5GB during execution
- **CPU**: Optimized for CPU inference (no GPU required)

## Troubleshooting

- **Model fails to load**: Check internet connection. Models download automatically on first run.
- **Docker build fails**: Ensure sufficient disk space (1GB minimum).
- **Out of memory**: Increase Docker memory allocation to 4GB.
- **Search returns no results**: DuckDuckGo API may be rate-limited. Try simpler queries or wait a few minutes.

## Architecture

- **planner.py**: Planner class that uses Flan-T5-Small to break goals into actionable steps
- **tools.py**: Implementation of search_web (DuckDuckGo) and summarize_text (DistilBART) tools
- **main.py**: CLI entry point and Executor class for running planned steps

## License

Apache 2.0

## Responsible Use

This tool uses a local language model for demonstration purposes. Do not rely on it for:
- Critical business decisions
- Medical or legal advice
- Tasks requiring high accuracy or real-time information

The tool is designed for educational and experimental use to showcase agentic AI planning concepts.