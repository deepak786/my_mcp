# How to connect to my MCP server from my client using langchain

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import asyncio
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

THIS_DIR = Path(__file__).parent
MY_MCP = str(THIS_DIR / "binance_mcp/binance_mcp.py")

mcp_config = {
    "binance": {
       "command": "python",
       "args": [MY_MCP],
       "transport": "stdio",
       "env": None,
    }
}

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

async def get_crypto_prices():
    async with MultiServerMCPClient(mcp_config) as client:
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        
        message = HumanMessage(content="What is the price of BTC?")
        
        response = await agent.ainvoke({"messages": [message]})
        answer = response["messages"][-1].content
        print(answer)

if __name__ == "__main__":
    asyncio.run(get_crypto_prices())