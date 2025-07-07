# How to connect to my MCP server from my client

from pathlib import Path
from mcp import ClientSession, StdioServerParameters, stdio_client

THIS_DIR = Path(__file__).parent
MCP_FOLDER = THIS_DIR / "binance_mcp"

server_params = StdioServerParameters(
    command="python",
    args=[str(MCP_FOLDER / "binance_mcp.py")],
    env=None,
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # initialize the session
            await session.initialize()
            
            # list the tools
            tools = await session.list_tools()
            print(tools)
            
            # get the price of the currency
            result = await session.call_tool("get_price", {"symbol": "BTC"})
            print(result)
        

if __name__ == "__main__":
    import asyncio # to run the async function
    asyncio.run(run())