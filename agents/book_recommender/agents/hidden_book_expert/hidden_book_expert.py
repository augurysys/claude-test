from langchain_community.vectorstores import FAISS

from agents.book_recommender.graph_state import GraphState
from utils.log_wrapper import LogWrapper


class HiddenBookExpert:
    def __init__(self,
                 logger: LogWrapper,
                 vectorstore: FAISS):
        self.logger = logger
        self.vectorstore = vectorstore

    def run(self, state: GraphState) -> dict[str, str]:
        query = state["question"]
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")

        self.logger.info(f"starting HiddenBookExpert with query: {query}")

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        retrieved_docs = retriever.invoke(query)

        result = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])

        self.logger.info(f"finished HiddenBookExpert with query: {result}")
        return {"hidden_book_expert_result": result}
