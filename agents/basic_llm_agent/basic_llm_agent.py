from langchain_core.prompts import ChatPromptTemplate

from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from utils.log_wrapper import LogWrapper


class BasicLlmAgent:
    AGENT_INSTRUCTIONS = (
        "You are a concise and helpful AI assistant. "
        "Answer the user's questions clearly and directly based on the information provided."
    )

    def __init__(self,
                 logger: LogWrapper,
                 azure_open_ai_wrapper: AzureOpenAIWrapper):

        self.logger = logger
        self.azure_open_ai_wrapper = azure_open_ai_wrapper

    def run(self, query: str) -> str:
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")

        self.logger.info(f"starting BasicLlmAgent with query: {query}")
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.AGENT_INSTRUCTIONS),
            ("human", "Question: {query} "),
        ])
        chain = chat_prompt_template | self.azure_open_ai_wrapper
        response = chain.invoke({"query": query})
        self.logger.info(f"finished BasicLlmAgent with query: {query}")

        return response.content