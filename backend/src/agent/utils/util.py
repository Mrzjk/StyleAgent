import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool
load_dotenv()
load_dotenv()
@tool
async def tavily_search(query: str,limit_k:int=5) -> str:
    """该工具可以搜索互联网上的信息."""
    api_key = os.getenv("TAVILY_API_KEY")
    tavily_client = TavilyClient(api_key = api_key)
    results = tavily_client.search(query)
    return results