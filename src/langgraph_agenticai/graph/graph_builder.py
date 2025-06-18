from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import tools_condition
from src.langgraph_agenticai.state.state import State
from src.langgraph_agenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agenticai.tools.search_tool import get_tools, create_tool_node
from src.langgraph_agenticai.nodes.chatbot_with_tool_node import ChatbotWithhTool


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



    
    def setup_graph(self,usecase:str):
        """
        Sets up the graph for the selected use case
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Tool":
            self.chatbot_with_tool_build_graph()
        return self.graph_builder.compile()