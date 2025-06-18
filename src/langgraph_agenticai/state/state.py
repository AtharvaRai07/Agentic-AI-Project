from typing_extensions import TypedDict, Annotated
from typing import List, Optional, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class State(TypedDict, total=False):
    messages: Annotated[List, add_messages]
    news_data: List[dict]  # 📰 To store Tavily results
    summary: str           # 📄 Final summary
    filename: str          # 💾 Saved file path
    frequency: str         # 🗓️ User input like 'daily', 'weekly'