# Create server parameters for stdio connection
from mcp import ClientSession
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
import asyncio
from config import MODEL_CONFIG
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate

# Enable verbose mode
from langchain.globals import set_verbose
set_verbose(True)

model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=MODEL_CONFIG["temperature"],
            max_tokens=MODEL_CONFIG["max_tokens"],
            api_key=MODEL_CONFIG["OPENAI_API_KEY"],
            base_url=MODEL_CONFIG["OPENAI_BASE_URL"]
    )

memory = MemorySaver()


prompt="you re a helpfull assistant"

MS = MultiServerMCPClient(
        {
            "server": {
                # make sure you start your weather server on port 8000
                "url": "http://127.0.0.1:8000/sse",
                "transport": "sse",
        }
        }
    )

async def run_agent():
    async with MS as client:
        # Get tools and create agent
        tools = client.get_tools()
        agent = create_react_agent(
            model,
            tools,
            prompt=prompt,
            checkpointer=memory,
            #debug=True
        )

        # Run interaction with memory
        config = {"configurable": {"thread_id": "math-session"}}
        print("Chat started. Type 'exit' to end the conversation.")
        
        # Initialize message history with system message
        messages = []
        
        while True:
            # Get user input
            user_input = input("You: ")
            
            # Check if user wants to exit
            if user_input.lower() == 'exit':
                print("Chat ended.")
                break
            
            # Add user message to history
            messages.append(("user", user_input))
            
            # Invoke agent with current message history
            result = await agent.ainvoke(
                {
                    "messages": messages
                },
                config
            )
            
            # Get assistant's response
            assistant_response = result["messages"][-1].content
            print(f"Assistant: {assistant_response}")
            
            # Add assistant response to history
            messages.append(("assistant", assistant_response))
        
        return "Chat session completed"

# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)