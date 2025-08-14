from langchain_community.vectorstores import FAISS
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from agents.book_recommender.agents.book_generator.book_generator import BookGeneratorAgent
from agents.book_recommender.agents.book_recommendation_summarizer.book_recommendation_summarizer import BookRecommendationSummarizerAgent
from agents.book_recommender.agents.hidden_book_expert.hidden_book_expert import HiddenBookExpert
from agents.book_recommender.graph_state import GraphState
from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from utils.log_wrapper import LogWrapper


class BookRecommenderGraph:
    def __init__(self,
                 logger: LogWrapper,
                 azure_open_ai_wrapper: AzureOpenAIWrapper,
                 vectorstore: FAISS):
        self.logger = logger
        self.azure_open_ai_wrapper = azure_open_ai_wrapper
        self.vectorstore = vectorstore

    def _initialize_agents(self):
        return {
            "book_generator": BookGeneratorAgent(self.logger, self.azure_open_ai_wrapper),
            "hidden_book_expert": HiddenBookExpert(self.logger, self.vectorstore),
            "book_recommendation_summarizer": BookRecommendationSummarizerAgent(self.logger, self.azure_open_ai_wrapper)
        }

    def _build_workflow(self, agents) -> StateGraph:
        workflow = StateGraph(GraphState)
        workflow = self._add_nodes(workflow, agents)
        workflow = self._add_edges(workflow)
        return workflow

    def _add_nodes(self, workflow, agents) -> StateGraph:
        workflow.add_node("book_generator", agents["book_generator"].run)
        workflow.add_node("hidden_book_expert", agents["hidden_book_expert"].run)
        workflow.add_node("book_recommendation_summarizer", agents["book_recommendation_summarizer"].run)
        return workflow

    def _add_edges(self, workflow) -> StateGraph:
        workflow.add_edge(START, "book_generator")
        workflow.add_edge("book_generator", "hidden_book_expert")
        workflow.add_edge("hidden_book_expert", "book_recommendation_summarizer")
        workflow.add_edge("book_recommendation_summarizer", END)
        return workflow

    def run(self, query):
        agents = self._initialize_agents()
        workflow = self._build_workflow(agents)
        app = workflow.compile()

        workflow_result = app.invoke({
            "logger": self.logger,
            "question": query
        })
        return workflow_result["final_book_recommendations"]
