# my mcp server

import os
from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
import requests
from pathlib import Path
from typing import Any
from datetime import datetime

THIS_DIR = Path(__file__).parent
ACTIVITY_LOG_FILE = THIS_DIR / "activity.log"

# MCP_HTTP is a boolean environment variable that determines if the MCP server should run in HTTP mode
# if it is true, the MCP server will run in HTTP mode, otherwise it will run in stdio mode
MCP_HTTP = os.getenv("MCP_HTTP", "false").lower() == "true"

port = int(os.environ.get("PORT", 7860))
mcp = FastMCP("Binance MCP", port=port) if MCP_HTTP else FastMCP("Binance MCP")

def get_symbol_from_name(name: str) -> str:
    if(name.lower() in ["btc", "bitcoin"]):
        return "BTCUSDT"
    elif(name.lower() in ["eth", "ethereum"]):
        return "ETHUSDT"
    elif(name.lower() in ["sol", "solana"]):
        return "SOLUSDT"
    elif(name.lower() in ["doge", "dogecoin"]):
        return "DOGEUSDT"
    else:
        return name.upper()

@mcp.tool()
def get_price(symbol: str) -> Any:
    """
    Get the price of a symbol from Binance

    Args:
        symbol (str): The symbol to get the price of. Example: "BTCUSDT"

    Returns:
        Any: The price of the symbol
    """
    
    symbol = get_symbol_from_name(symbol)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    if(response.status_code != 200):
        # log the error to the activity.log file
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(f"{datetime.now()}: Error getting price for {symbol}: {response.status_code} {response.text}\n")
        # raise an exception to the caller
        raise Exception(f"Error getting price for {symbol}: {response.status_code} {response.text}")
    else:
        # log the success to the activity.log file
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(f"{datetime.now()}: Successfully got price for {symbol}: {response.json()}\n")
    return response.json()

@mcp.tool()
def get_price_change(symbol: str) -> Any:
    """
    Get the price change of a symbol from Binance for the last 24 hours

    Args:
        symbol (str): The symbol to get the price change of. Example: "BTCUSDT"

    Returns:
        Any: The price change of the symbol
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    if(response.status_code != 200):
        # log the error to the activity.log file
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(f"{datetime.now()}: Error getting price change for {symbol}: {response.status_code} {response.text}\n")
        # raise an exception to the caller
        raise Exception(f"Error getting price change for {symbol}: {response.status_code} {response.text}")
    else:
        # log the success to the activity.log file
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(f"{datetime.now()}: Successfully got price change for {symbol}: {response.json()}\n")
    return response.json()

# MCP Resource to get the activity log
@mcp.resource("file://activity.log")
def get_activity_log() -> Any:
    """
    Get the activity log
    """
    return ACTIVITY_LOG_FILE.read_text()

@mcp.resource("file://symbol_map.csv")
def symbol_map() -> str:
    return """
        crypto_name,symbol
        btc,BTCUSDT
        eth,ETHUSDT
        bitcoin,BTCUSDT
        my_favorite,ETCUSDT
    """
    
@mcp.prompt()
def cypto_summary(crypto_name: str) -> str:
    """
    Get the summary of a crypto currency
    """
    return f"""
        get the price of the currency: {crypto_name}
        and the price change of the currency for the last 24 hours.
        give me the summary in a markdown format.
    """

if __name__ == "__main__":
    # create activity.log file if it doesn't exist
    if(not Path(ACTIVITY_LOG_FILE).exists()):
        Path(ACTIVITY_LOG_FILE).touch()
    # start the MCP server
    mcp.run(transport="streamable-http" if MCP_HTTP else "stdio")
    
# npx @modelcontextprotocol/inspector /Users/deepakgoyal/Desktop/Workspace/00Samples/MCP/.venv/bin/python /Users/deepakgoyal/Desktop/Workspace/00Samples/MCP/binance_mcp/binance_mcp.py
# mcp dev binance_mcp/binance_mcp.py