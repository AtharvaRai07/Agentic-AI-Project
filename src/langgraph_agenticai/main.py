import streamlit as st
from src.langgraph_agenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraph_agenticai.LLMs.groq_llm import GroqLLM
from src.langgraph_agenticai.graph.graph_builder import GraphBuilder
from src.langgraph_agenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from langgraph.checkpoint.memory import MemorySaver

def load_langgraph_agenticai_app():
    # Load sidebar config UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    # Stop early if no inputs selected
    if not user_input:
        st.warning("Please select LLM and Use Case.")
        st.stop()

    # 🧠 Setup per-user memory
    if "memory" not in st.session_state:
        st.session_state.memory = MemorySaver()

    # User sends input
    user_message = st.chat_input("Enter your message here") 
    if user_message:
        try:
            # Initialize LLM based on selected config
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Failed to initialize LLM model.")
                return

            # Get selected usecase
            usecase = user_input.get("selected_usercase")
            if not usecase:
                st.error("Please select a usecase.")
                return

            # 🧠 Build graph with memory
            graph_builder = GraphBuilder(model=model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error setting up graph: {e}")
                return
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
