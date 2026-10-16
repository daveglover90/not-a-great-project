"""Low-level MCP client using the official `mcp` Python SDK (ClientSession + stdio_client)."""
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["mcp_servers/math_server.py"],
)


async def run() -> None:
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])
            result = await session.call_tool("add", arguments={"a": 2, "b": 40})
            print("add(2, 40) =", result.content[0].text)


if __name__ == "__main__":
    asyncio.run(run())
