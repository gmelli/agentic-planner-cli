# Current Tool Extension Pattern

## Current Architecture (Simple & Working)

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Planner       │    │   Tools Class    │    │   Tool Methods  │
│ (Flan-T5-Small)│───▶│   (tools.py)     │◀───│   (2 built-in)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Executor      │    │   Context Dict   │    │   search_web    │
│   (main.py)     │───▶│   (simple)       │    │   summarize_text│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## How to Add New Tools (Current Implementation)

### Step 1: Add Tool Method to tools.py
```python
def my_new_tool(self, argument: str) -> str:
    """Your tool implementation.
    
    Args:
        argument: Input string from planner
        
    Returns:
        Result string for next step or final output
    """
    try:
        # Your tool logic here
        result = do_something(argument)
        return result
    except Exception as e:
        return f"Tool failed: {str(e)}"
```

### Step 2: Register in execute_tool() Method
```python
def execute_tool(self, tool_name: str, argument: str) -> str:
    if tool_name == "search_web":
        return self.search_web(argument)
    elif tool_name == "summarize_text":
        return self.summarize_text(argument)
    elif tool_name == "my_new_tool":  # Add this line
        return self.my_new_tool(argument)
    else:
        return f"Unknown tool: {tool_name}"
```

### Step 3: Update Planner Recognition
```python
# In planner.py _parse_steps() method
if 'my_new_tool' in line.lower():
    steps.append({'tool': 'my_new_tool', 'argument': extracted_argument})
```

## Current Tool Examples

### Implemented Tools
- **search_web**: DuckDuckGo API with retry logic
- **summarize_text**: DistilBART with text truncation

### Tool Requirements
- **Input**: Single string argument
- **Output**: String result (chainable)
- **Error handling**: Return error messages as strings, don't raise exceptions
- **Stateless**: Don't maintain state between calls

## Context Management (Current)
```python
# In executor.py
self.context = {
    'last_search_result': result,  # Available for summarization
    'step_1_result': result,       # Historical results
    f'step_{i+1}_result': result   # Sequential numbering
}
```

## Extension Ideas for Future

### Information Retrieval
- **search_local**: Search local file system
- **fetch_url**: Direct URL content retrieval
- **query_database**: SQL database queries

### Text Processing  
- **translate_text**: Language translation
- **extract_entities**: Named entity recognition
- **analyze_sentiment**: Sentiment analysis

### Output Generation
- **save_file**: Write results to disk
- **format_report**: Structure data into reports
- **send_notification**: Alert mechanisms

## Why This Simple Pattern Works

1. **Proven**: Successfully demonstrates agentic planning
2. **Testable**: Easy to mock and unit test
3. **Understandable**: Clear flow from goal to result
4. **Maintainable**: Minimal complexity, easy to debug
5. **Extensible**: New tools can be added in minutes

## Migration Path (If Needed)

If the tool set grows beyond ~10 tools, consider:
1. Move to plugin directory structure
2. Add automatic tool discovery
3. Implement schema validation
4. Add dependency management

**Current verdict**: The simple pattern serves the educational and demo purposes perfectly. Keep it simple until complexity is actually needed.