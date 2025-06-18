from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Returns the tools for the chatbot
    """
    tools = [TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """
    Returns the tool node for the chatbot
    """
    tool_node = ToolNode(tools)
    return tool_node