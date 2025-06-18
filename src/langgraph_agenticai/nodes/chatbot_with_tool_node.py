from src.langgraph_agenticai.state.state import State

class ChatbotWithhTool:

    def __init__(self,model):
        self.llm = model

    def chatbot(self,tools):
        """
        Chatbot with tool use case
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state:State):
            """
            Chatbot logic for procesing the input state and returning a repsonse
            """
            return {"messages":[llm_with_tools.invoke(state['messages'])]}
        
        return chatbot_node