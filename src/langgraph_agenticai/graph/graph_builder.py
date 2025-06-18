from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import tools_condition
from src.langgraph_agenticai.state.state import State
from src.langgraph_agenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraph_agenticai.nodes.chatbot_with_tool_node import ChatbotWithhTool
from src.langgraph_agenticai.nodes.ai_news_node import AINewsNode


class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tool_build_graph(self):
        """
        Builds the graph for the chatbot with tool use case
        """
        tools =  get_tools()
        tool_node = create_tool_node(tools)

        llm = self.llm
        obj_chatbot_with_node = ChatbotWithhTool(llm)
        chatbot_node = obj_chatbot_with_node.chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition
        )
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder(self):
        """
        Builds the graph for the ai news use case
        """
        obj_ainews = AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news",obj_ainews.fetch_news)
        self.graph_builder.add_node("summarize_news", obj_ainews.summarize_news)
        self.graph_builder.add_node("save_reuslt",obj_ainews.save_result)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_reuslt")
        self.graph_builder.add_edge("save_reuslt", END)

    
    def setup_graph(self,usecase:str):
        """
        Sets up the graph for the selected use case
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Tool":
            self.chatbot_with_tool_build_graph()
        if usecase == "AI News":
            self.ai_news_builder()
        return self.graph_builder.compile()