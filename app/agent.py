"""LangGraph agent wired to three MCP servers via langchain-mcp-adapters.

AI-BOM should show: application -> mcp-client -> {MathServer, NotesServer, WeatherServer} -> tools,
plus the foundation models used to drive the agent.
"""
import asyncio
import os

from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

PRIMARY_MODEL = "openai:gpt-4.1"
FALLBACK_MODEL = "anthropic:claude-sonnet-4-5"


def build_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mcp_servers/math_server.py"],
                "transport": "stdio",
            },
            "notes": {
                "command": "python",
                "args": ["mcp_servers/notes_server.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )


async def main(question: str) -> None:
    model_name = PRIMARY_MODEL if os.getenv("OPENAI_API_KEY") else FALLBACK_MODEL
    model = init_chat_model(model_name, temperature=0)

    client = build_client()
    tools = await client.get_tools()
    agent = create_react_agent(model, tools)

    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main("What's (3 + 5) x 12, and what's the weather in Hartford?"))
