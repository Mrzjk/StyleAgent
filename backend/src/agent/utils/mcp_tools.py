from langchain_mcp_adapters.client import MultiServerMCPClient
from agent.config.mcp_config import mcp_config

async def get_mcp_tools(mcp_config:dict)->list:
    mcp_client = MultiServerMCPClient(mcp_config)
    tools = await mcp_client.get_tools()
    return tools