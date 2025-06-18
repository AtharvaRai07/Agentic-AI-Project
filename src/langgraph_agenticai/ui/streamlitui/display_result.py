import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase == "Basic Chatbot":

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # Save user message
            st.session_state.chat_history.append(("user", user_message))

            # Process through LangGraph
            response_text = None
            for event in graph.stream({"messages": ("user", user_message)}):
                for value in event.values():
                    # Handle AIMessage list properly
                    if isinstance(value["messages"], list):
                        last_message = value["messages"][-1]
                        response_text = last_message.content if hasattr(last_message, 'content') else last_message
                    else:
                        response_text = value["messages"]

            # Save assistant response
            if response_text:
                st.session_state.chat_history.append(("assistant", response_text))

            # 🔁 Display chat history
            for role, message in st.session_state.chat_history:
                with st.chat_message(role):
                    st.write(message)

        elif usecase == "Chatbot with Tool":

            # ✅ Initialize session state for tool-based messages
            if "messages" not in st.session_state:
                st.session_state["messages"] = []

            # Add user's new input to message history
            initial_state = {"messages": st.session_state["messages"] + [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)

            # Iterate and display
            for message in res["messages"]:
                if isinstance(message, HumanMessage):
                    st.session_state["messages"].append(message)
                    with st.chat_message("user"):
                        st.write(message.content)

                elif isinstance(message, ToolMessage):
                    st.session_state["messages"].append(message)
                    with st.chat_message("ai"):
                        st.write("🔧 Tool Call Start")
                        st.write(message.content)
                        st.write("🔧 Tool Call End")

                elif isinstance(message, AIMessage) and message.content:
                    st.session_state["messages"].append(message)
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


            

