from langchain_core.prompts import ChatPromptTemplate

from agents.book_recommender.graph_state import GraphState
from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from utils.log_wrapper import LogWrapper


class BookGeneratorAgent:
    AGENT_INSTRUCTIONS = (
        "You are a creative book recommender AI. "
        "Recommend fictional books that fit the user's mood or theme."
        "Choose 15 books"
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

        self.logger.info(f"starting BookGeneratorAgent with query: {query}")

        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.AGENT_INSTRUCTIONS),
            ("human", f"User mood/theme: {query} "),
        ])
        chain = chat_prompt_template | self.azure_open_ai_wrapper
        response = chain.invoke({"query": query})
        self.logger.info(f"finished BookGeneratorAgent with query: {query}")

        return {"book_generator_result": response.content}
