from langchain_core.prompts import ChatPromptTemplate

from agents.book_recommender.graph_state import GraphState
from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from utils.log_wrapper import LogWrapper


class BookRecommendationSummarizerAgent:
    AGENT_INSTRUCTIONS = (
        "You are a creative book recommender AI. "
        "You are given a list of books and their summary. Choose the top 3 books based on the user requested theme."
        "Include a short and concise reasoning about your choice."
        "Always prefer books from internal sources if they make sense"
    )

    def __init__(self,
                 logger: LogWrapper,
                 azure_open_ai_wrapper: AzureOpenAIWrapper):
        self.logger = logger
        self.azure_open_ai_wrapper = azure_open_ai_wrapper

    def run(self, state: GraphState) -> dict[str, str]:
        query = state["question"]
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")

        self.logger.info(f"starting BookRecommendationSummarizerAgent with query: {query}")

        book_generator_result = state["book_generator_result"]
        hidden_book_expert_result = state["hidden_book_expert_result"]
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.AGENT_INSTRUCTIONS),
            ("human", "Available books: {book_generator_result} --- "),
            ("human", "Books from internal sources: {hidden_book_expert_result} --- "),
            ("human", "User mood/theme: {query} "),
        ])
        chain = chat_prompt_template | self.azure_open_ai_wrapper
        response = chain.invoke({"query": query, "book_generator_result": book_generator_result, "hidden_book_expert_result": hidden_book_expert_result})
        self.logger.info(f"finished BookRecommendationSummarizerAgent with query: {query}")

        return {"final_book_recommendations": response.content}
