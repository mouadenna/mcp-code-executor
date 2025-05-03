# MCP Code Executor

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A powerful and secure Model Context Protocol (MCP) server that executes code in multiple programming languages. Designed for AI assistants to safely run code snippets and return formatted results through a standardized interface.

## 🚀 Features

- **Multi-language support**: Execute code in multiple programming languages
- **Secure execution**: Isolated environments with configurable resource limits
- **Docker integration**: Run in containers for enhanced security and portability
- **MCP compatible**: Seamlessly integrates with Claude and other MCP-enabled AI assistants
- **Structured output**: Standardized response format with stdout, stderr, exit codes, and execution metadata

## 💻 Supported Languages

| Language | Version | Support Level |
|----------|---------|--------------|
| Python | 3.10+ | Full |
| JavaScript (Node.js) | 16+ | Full |
| TypeScript | 4+ | Full |
| Java | JDK 11+ | Full |
| C++ | C++17 | Full |
| Bash | 5.0+ | Full |

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js and npm (for JavaScript/TypeScript execution)
- JDK 11 or higher (for Java execution)
- g++ compiler (for C++ execution)
- Docker (optional, for containerized execution)

## 🔧 Installation

### Option 1: Standard Installation

```bash
# Clone the repository
git clone https://github.com/your-username/mcp-code-executor.git
cd mcp-code-executor

# Install dependencies
pip install -r requirements.txt

# Run the server
python code_executor_server.py
```

### Option 2: Docker Installation

```bash
# Clone the repository
git clone https://github.com/your-username/mcp-code-executor.git
cd mcp-code-executor

# Build and start with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t mcp-code-executor .
docker run -p 8000:8000 mcp-code-executor
```

### MCP Integration

```bash
# For development with the MCP Inspector
mcp dev code_executor_server.py

# To install in Claude Desktop
mcp install code_executor_server.py
```

## 📖 Usage

### API Reference

The server exposes code execution capabilities through the MCP protocol. To use it, you'll need to connect to it with an MCP client.

#### Client Setup

The repository includes a sample client (`client.py`) that connects to the MCP server and allows you to interact with it through a chat interface:

```python
# Import required libraries
from mcp import ClientSession
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
import asyncio
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# Set up the LLM model
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# Set up memory for the agent
memory = MemorySaver()

# Configure the MCP client to connect to the server
client = MultiServerMCPClient(
    {
        "server": {
            "url": "http://127.0.0.1:8000/sse",
            "transport": "sse",
        }
    }
)
```

#### Connecting to the Server

To connect to the server and use its tools:

```python
async def run_agent():
    async with client as mcp_client:
        # Get tools from the server
        tools = mcp_client.get_tools()
        
        # Create an agent with the tools
        agent = create_react_agent(
            model,
            tools,
            prompt="You're a helpful assistant that can execute code."
        )
        
        # Run the agent with a user query
        result = await agent.ainvoke(
            {
                "messages": [
                    ("user", "Run this Python code: print('Hello World!')")
                ]
            }
        )
        
        # Display the result
        print(result["messages"][-1].content)

# Run the agent
asyncio.run(run_agent())
```

### Running the Client

To start the client and interact with the code execution server:

```bash
# Make sure the server is running first
python code_executor_server.py

# In a separate terminal, run the client
python client.py
```

## 📝 Examples

When interacting with the client, you can ask it to execute code in various languages. Here are some examples of conversations with the client:

### Python Example

```
You: Can you execute this Python code for me?
```python
import math

def calculate_circle_area(radius):
    return math.pi * radius ** 2

print(f"Area of circle with radius 5: {calculate_circle_area(5):.2f}")
```

## 🔒 Security Considerations

This service executes arbitrary code, which inherently carries security risks. We've implemented several layers of protection:

- **Execution time limits**: All code is limited to 10 seconds execution time
- **Docker isolation**: When run in Docker, code executes in an isolated container
- **Temporary file usage**: All code runs in temporary directories that are removed after execution
- **No network access**: Execution environments can be configured to restrict network access

### Additional Security Recommendations

- Run behind an authentication layer in production environments
- Configure resource limits (CPU, memory) in production Docker deployments
- Use read-only file systems where possible
- Monitor for abuse patterns and implement rate limiting
- Keep all dependencies updated regularly

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.