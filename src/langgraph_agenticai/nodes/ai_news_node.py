from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from src.langgraph_agenticai.state.state import State  # <-- your State class with news_data, summary, etc.

class AINewsNode:
    def __init__(self, llm):
        self.tavily = TavilyClient()
        self.llm = llm

    def fetch_news(self, state: State) -> State:
        # Extract frequency from last message
        frequency = state['messages'][-1].content.lower()
        state['frequency'] = frequency

        # Map for Tavily API
        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm'}
        days_map = {"daily": 1, "weekly": 7, "monthly": 30}

        # Call Tavily API
        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news in the world",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
        )

        # Save results into state
        state['news_data'] = response.get('results', [])
        print(f"[fetch_news] {len(state['news_data'])} articles fetched.")
        return state

    def summarize_news(self, state: State) -> State:

        news_content = state['news_data']

        # Prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system",
                "You are an expert news summarizer. Given a list of recent AI-related news articles, your task is to summarize them clearly, concisely, and professionally. Group similar topics together where appropriate."),
            ("human",
                "Here are the news articles:\n\n{news_articles}\n\nSummarize the key points in a bullet list format.")
        ])

        # Format articles
        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_content
        ])

        # Invoke LLM
        response = self.llm.invoke(prompt_template.format(news_articles=articles_str))
        state['summary'] = response.content
        print(f"[summarize_news] Summary generated.")
        return state

    def save_result(self, state: State) -> State:
        frequency = state.get('frequency', 'unknown')
        summary = state.get('summary', '')

        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        state['filename'] = filename
        print(f"[save_result] Summary saved to {filename}")
        return state
