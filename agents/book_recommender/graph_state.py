from typing import TypedDict

from utils.log_wrapper import LogWrapper


class GraphState(TypedDict):
    question: str
    logger: LogWrapper

    book_generator_result: str
    hidden_book_expert_result: str
    final_book_recommendations: str



