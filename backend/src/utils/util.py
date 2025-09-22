import os
from tavily import TavilyClient
from dotenv import load_dotenv
from langchain.tools import tool


load_dotenv()
@tool
def search_web(query:str)->str:
    client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))