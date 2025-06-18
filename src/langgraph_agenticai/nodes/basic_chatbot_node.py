from src.langgraph_agenticai.state.state import State


class BasicChatbotNode:
    """
    Basic Chatbot login implentation
    """
    def __init__(self,model):
        self.llm = model

    def process(self,state:State)->dict:
        """"
        Process the input state and generate a chatbot response
        """
        return {"messages":self.llm.invoke(state["messages"])}