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
   docker run --rm agentic-planner-cli "explain quantum computing to me"
   ```

## Usage Examples

### Individual Commands

```bash
# Conversational research requests
docker run --rm agentic-planner-cli "explain quantum computing to me"
docker run --rm agentic-planner-cli "help me understand machine learning"
docker run --rm agentic-planner-cli "what should I know about blockchain"

# Show AI reasoning with explain mode
docker run --rm agentic-planner-cli "teach me about neural networks" --explain

# Use lite model profile for lower resource usage
docker run --rm agentic-planner-cli "give me an overview of artificial intelligence" --model-profile lite

# Verbose output shows all execution details
docker run --rm agentic-planner-cli "summarize edge computing for beginners" --verbose
```

### Interactive Demo Script

For a guided demonstration with clear separation between examples:

```bash
# Run interactive demo with explanations
./run-samples.sh
```

This script runs each example with:
- Clear headers and separators
- Pause between demonstrations  
- Explanations of what each sample showcases
- Professional output formatting

## Command Line Options

- `goal`: The goal you want to achieve (required)
- `--max-steps N`: Maximum number of steps to execute (default: 10)
- `--verbose, -v`: Enable verbose output showing planning and execution details
- `--explain`: Show how the AI decomposes the goal (includes --verbose)
- `--model-profile {lite|full}`: Choose resource profile (default: full)
  - **lite**: ~1.2GB RAM, ~450MB disk (optimized inference)
  - **full**: ~1.5GB RAM, ~550MB disk (standard configuration)

## Available Tools

The planner can use these built-in tools:

- **search_web(query)**: Searches the web using DuckDuckGo API
- **summarize_text(text)**: Generates a concise summary using DistilBART

## Sample Outputs

### Planning Quality Comparison

**DistilGPT-2 (Previous)**:
```
Goal: "Research quantum computing trends"
Plan: "search_web(latest news) summarize_text(search results)"
Issues: Generic "latest news" regardless of goal, poor instruction following
```

**Flan-T5-Small (Current)**:
```
Goal: "Research quantum computing trends"
Plan: "Step 1: search_web(quantum computing trends research)
       Step 2: summarize_text(search results)"
Improvements: Goal-specific queries, structured step format, reliable parsing
```

### Execution Example

```bash
$ docker run --rm agentic-planner-cli "explain quantum computing to me" --explain

[PLANNER] Loading Flan-T5-Small (80M parameters)
[INFERENCE] Generating plan for goal: explain quantum computing to me
[PLAN] Step 1: search_web(quantum computing)
[PLAN] Step 2: summarize_text(search results)

[EXECUTOR] Executing Step 1: search_web
[SEARCH] Querying DuckDuckGo API
[QUERY] 'quantum computing'
[DATA] Found abstract: 1075 chars
[COMPLETE] Search finished: 3 sections, 1075 chars

[EXECUTOR] Executing Step 2: summarize_text
[SUMMARIZE] Processing text with DistilBART
[OUTPUT] Summary generated: 284 characters

[RESULT] A quantum computer exploits superposed and entangled states and the outcomes of quantum measurements as features of its computation. Ordinary computers operate using deterministic rules. A large-scale quantum computer could break widely used encryption schemes.
```

## Extending the CLI

### Adding New Tools

The tool system uses a simple plugin pattern. To add a new tool:

1. **Add the tool method** to `tools.py`:
```python
def my_new_tool(self, argument: str) -> str:
    """Your tool implementation."""
    return "tool result"
```

2. **Register in execute_tool()** method:
```python
def execute_tool(self, tool_name: str, argument: str) -> str:
    if tool_name == "my_new_tool":
        return self.my_new_tool(argument)
    # ... existing tools
```

3. **Update the planner** to recognize your tool in `planner.py` `_parse_steps()`:
```python
if 'my_new_tool' in line.lower():
    steps.append({'tool': 'my_new_tool', 'argument': extracted_argument})
```

### Tool Requirements

- **Input**: Single string argument
- **Output**: String result (for chaining between steps)
- **Error handling**: Return error messages as strings, don't raise exceptions
- **Context**: Access previous results via `self.context` in executor

### Available Tool Slots

The current architecture supports these tool categories:
- **Information retrieval**: search_web, search_local, fetch_data
- **Processing**: summarize_text, translate_text, analyze_sentiment  
- **Output**: save_file, send_notification, format_report

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

The project includes both unit tests (mocked) and integration tests (real APIs):

```bash
# Fast unit tests (offline, mocked dependencies)
python -m pytest tests/test_*.py -v -k "not integration"

# Integration tests (real API calls, Docker required)
python -m pytest tests/test_integration.py -v

# All tests
python -m pytest tests/ -v
```

#### Testing Strategy

**Unit Tests** (`test_planner.py`, `test_tools.py`, `test_main.py`):
- **Model Mocking**: Mock `transformers.pipeline` to avoid model downloads during CI
- **Network Mocking**: Mock `requests.get` for predictable API responses
- **Coverage**: Test success/failure scenarios for all components
- **CI-Friendly**: Run offline, no external dependencies

**Integration Tests** (`test_integration.py`):
- **Real API calls**: Test actual DuckDuckGo API responses and field priority
- **Docker end-to-end**: Verify complete containerized workflow
- **README validation**: Ensure documented examples actually work
- **Performance**: Verify acceptable response times under real conditions

#### Why Both Are Needed

The DuckDuckGo API parsing bug demonstrated the gap between unit and integration testing:
- **Unit tests**: Caught logic errors but missed API field priority (`Answer` vs `Abstract`)
- **Integration tests**: Would have caught "No detailed results found" failures immediately

Example of real API testing in `test_integration.py`:
```python
def test_api_quantum_computing_response(self):
    # Makes real API call to verify field structure
    response = requests.get(self.api_url, params={'q': 'quantum computing'})
    data = response.json()
    self.assertTrue(data.get('Abstract'))  # Real API behavior
    self.assertFalse(data.get('Answer'))   # Catches field priority bugs
```

## Resource Requirements

### System Requirements
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: Any modern x86_64 or ARM64 processor
- **Disk**: 1GB free space (500MB for models + 500MB for container)
- **Network**: Internet connection for initial model download and web search

### Model Details
- **Flan-T5-Small**: 80M parameters, ~300MB download (planning)
- **DistilBART-CNN**: 306M parameters, ~250MB download (summarization)  
- **Total**: 386M parameters, ~550MB disk usage

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

## References

This implementation draws from research in agentic AI systems and command-line interface design:

1. **Agentic Planning CLI Tool** - Conceptual framework and design principles  
   https://www.gabormelli.com/RKB/Agentic_Planning_CLI_Tool

2. **Command-Line Interface** - Foundational CLI design concepts  
   https://www.gabormelli.com/RKB/CLI-based_Program

3. **Agentic CLI Tools Compared** - Contemporary analysis of AI-powered CLI tools  
   https://research.aimultiple.com/agentic-cli

## License

Apache 2.0

## Responsible Use

This tool uses a local language model for demonstration purposes. Do not rely on it for:
- Critical business decisions
- Medical or legal advice
- Tasks requiring high accuracy or real-time information

The tool is designed for educational and experimental use to showcase agentic AI planning concepts.