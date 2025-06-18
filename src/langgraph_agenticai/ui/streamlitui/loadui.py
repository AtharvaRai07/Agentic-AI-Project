import os
import streamlit as st
from src.langgraph_agenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(),layout="wide")
        st.header("🤖 " + self.config.get_page_title(), divider="rainbow")
        st.session_state.time_frame =''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            st.title("🛠️ Configuration")
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            self.user_controls['selected_usercase'] = st.selectbox("Select Use Case", usecase_options)

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls['selected_groq_model'] = st.selectbox("Select Groq Model", model_options)
                self.user_controls['GROQ_API_KEY'] = st.session_state['GROQ_API_KEY'] = st.text_input("Enter Groq API Key", type="password")
                if not self.user_controls['GROQ_API_KEY']:
                    st.warning("Please enter your Groq API Key. Don't have refer: https://console.groq.com/keys")
                    st.stop()

            if self.user_controls['selected_usercase'] == "Chatbot with Tool" or self.user_controls['selected_usercase'] == "AI News":
                os.environ['TAVILY_API_KEY'] = self.user_controls["TAVILY_API_KEY"] = st.session_state['TAVILY_API_KEY'] = st.text_input("Enter Tavily API Key", type="password")
                if not self.user_controls['TAVILY_API_KEY']:
                    st.warning("Please enter your Tavily API Key. Don't have refer: https://app.tavily.com/home")
                    st.stop()
            
            if self.user_controls['selected_usercase'] == "AI News":
                st.subheader("📃 Select Time Frame")
                with st.sidebar:
                    time_frame = st.selectbox("Select Time Frame", ["Daily", "Weekly", "Monthly"],index=0)
                if st.button("🔎 Fetch Latest AI News",use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.time_frame = time_frame

        return self.user_controls

