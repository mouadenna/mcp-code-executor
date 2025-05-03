# MCP Code Executor

A Model Context Protocol (MCP) server that provides a code execution tool. This server allows executing code in various programming languages and returns the output or errors.

## Supported Languages
- Python
- JavaScript (Node.js)
- TypeScript
- Java
- C++
- Bash

## Installation

### Standard Installation

1. Install the dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python code_executor_server.py
```

### Docker Installation

1. Build and start the Docker container:
```bash
docker-compose up -d
```

2. Or build and run the Docker image manually:
```bash
docker build -t mcp-code-executor .
docker run -p 8000:8000 mcp-code-executor
```

### MCP Tools

1. For development with the MCP Inspector:
```bash
mcp dev code_executor_server.py
```

2. To install in Claude Desktop:
```bash
mcp install code_executor_server.py
```

## Usage

Use the `execute_code` tool with the following parameters:
- `language`: The programming language to use (python, javascript, typescript, java, cpp)
- `code`: The code to execute

The tool returns:
- `output`: Standard output from the code execution
- `error`: Standard error output or execution errors
- `exitCode`: Exit code of the execution
- `timeout`: Boolean indicating if the execution timed out

## Examples

### Python Example
```python
result = execute_code(
    language="python",
    code="print('Hello, world!')"
)
# Result: {"output": "Hello, world!", "error": "", "exitCode": 0, "timeout": false}
```

### JavaScript Example
```javascript
result = execute_code(
    language="javascript",
    code="console.log('Hello from Node.js');"
)
# Result: {"output": "Hello from Node.js\n", "error": "", "exitCode": 0, "timeout": false}
```

### Java Example
```java
result = execute_code(
    language="java",
    code="""
    public class Main {
        public static void main(String[] args) {
            System.out.println("Hello from Java!");
        }
    }
    """
)
# Result: {"output": "Hello from Java!\n", "error": "", "exitCode": 0, "timeout": false}
```

## Security Notice

This server executes arbitrary code, which can pose security risks. It's recommended to:
- Run in a sandboxed environment (using Docker is recommended for isolation)
- Limit execution time (currently set to 10 seconds)
- Add proper authentication if exposing to a network
- Apply resource restrictions in production environments

## Docker Security Considerations

When running in Docker:
- The container has limited resources
- Processes run in isolation from the host
- Consider adding additional security measures like read-only file systems for production deployments