"""MCP server exposed over streamable HTTP, so the AI-BOM shows a remote (non-stdio) server too.

Run:  python mcp_servers/weather_server.py   (listens on http://localhost:8000/mcp)
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WeatherServer")


@mcp.tool()
def get_forecast(city: str) -> str:
    """Return a canned weather forecast for a city."""
    return f"Forecast for {city}: 62F, light wind, clear skies."


@mcp.resource("weather://cities")
def supported_cities() -> str:
    """List of supported cities."""
    return "Boston, Hartford, New York, Denver"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
