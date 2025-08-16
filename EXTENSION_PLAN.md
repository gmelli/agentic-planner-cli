# Extensible Tool Framework Design

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Planner       │    │   Tool Registry  │    │   Tool Plugins  │
│ (Flan-T5-Small)│───▶│   & Validator    │◀───│   (Extensible)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Executor      │    │   Context Mgmt   │    │   Built-in +    │
│   (Orchestrator)│───▶│   & State        │    │   Custom Tools  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Core Components

### 1. Tool Registry System
```python
class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.schemas = {}
    
    def register_tool(self, name: str, func: callable, schema: dict):
        # Validate tool function signature
        # Store tool with input/output schema
        pass
    
    def get_available_tools(self) -> List[str]:
        # Return list of tool names for planner prompt
        pass
    
    def execute_tool(self, name: str, **kwargs) -> dict:
        # Execute with validation and error handling
        pass
```

### 2. Tool Plugin Interface
```python
from abc import ABC, abstractmethod

class ToolPlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        pass
    
    @property
    @abstractmethod
    def schema(self) -> dict:
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> dict:
        pass
```

### 3. Enhanced Context Management
```python
class ExecutionContext:
    def __init__(self):
        self.variables = {}
        self.step_history = []
        self.tool_outputs = {}
    
    def store_result(self, step_id: str, tool: str, result: any):
        # Store with metadata and type information
        pass
    
    def resolve_variable(self, var_name: str) -> any:
        # Resolve context variables like ${last_search}
        pass
```

## Implementation Steps

### Phase 1: Core Framework
1. Create `tool_registry.py` with registration system
2. Define `tool_plugin.py` base class
3. Refactor existing tools to use plugin interface
4. Update planner to use registry for available tools

### Phase 2: Plugin System
1. Create `plugins/` directory structure
2. Implement plugin discovery and loading
3. Add tool validation and schema checking
4. Create example plugins (file_io, calculator, etc.)

### Phase 3: Advanced Features
1. Variable interpolation in tool arguments (${previous_result})
2. Conditional execution based on tool outputs
3. Parallel tool execution where safe
4. Tool dependency management

## Example Plugin Structure

```
plugins/
├── __init__.py
├── file_operations.py     # read_file, write_file, list_directory
├── calculations.py        # calculate, convert_units
├── web_extended.py        # parse_html, extract_links
└── data_processing.py     # filter_data, transform_json
```

## Benefits
- **Modularity**: Tools as independent, testable components
- **Extensibility**: Easy addition of domain-specific tools
- **Validation**: Schema-based input/output checking
- **Discovery**: Automatic tool detection and registration
- **Maintainability**: Clear separation of concerns