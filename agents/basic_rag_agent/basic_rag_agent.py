from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from utils.log_wrapper import LogWrapper


class BasicRagAgent:
    AGENT_INSTRUCTIONS = (
        "You are a concise and helpful AI assistant. "
        "Answer the user's questions clearly and directly based on the information provided."
    )

    def __init__(self,
                 logger: LogWrapper,
                 azure_open_ai_wrapper: AzureOpenAIWrapper,
                 vectorstore: FAISS):
        self.logger = logger
        self.azure_open_ai_wrapper = azure_open_ai_wrapper
        self.vectorstore = vectorstore

    def run(self, query: str) -> str:
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")

        self.logger.info(f"starting BasicRagAgent with query: {query}")

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        retrieved_docs = retriever.invoke(query)

        context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])

        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.AGENT_INSTRUCTIONS),
            ("human", "Additional Context: {context} -------"),
            ("human", "Question: {query} "),
        ])
        chain = chat_prompt_template | self.azure_open_ai_wrapper
        response = chain.invoke({"query": query, "context": context})
        self.logger.info(f"finished BasicRagAgent with query: {query}")

        return response
