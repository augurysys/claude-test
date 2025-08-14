from langchain_core.output_parsers import PydanticOutputParser

from agents.ecommerce_support_agent.prompts.example_few_shots import ECOMMERCE_SUPPORT_FEW_SHOTS
from core.few_shots_generator import FewShotsGenerator
from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from models.ecommerce_support_response_request import EcommerceSupportResponse
from utils.log_wrapper import LogWrapper


class EcommerceSupportAgent:
    AGENT_INSTRUCTIONS = (
        "You are a customer support agent for an e-commerce company. You are helping a customer with their queries."
    )

    def __init__(self,
                 logger: LogWrapper,
                 azure_open_ai_wrapper: AzureOpenAIWrapper):
        self.logger = logger
        self.azure_open_ai_wrapper = azure_open_ai_wrapper

    def run(self, query: str, domain_data) -> dict:
        if not query or not isinstance(query, str):
            raise ValueError("query must be a non-empty string")

        self.logger.info(f"starting EcommerceSupportAgent with query: {query}")

        parser = PydanticOutputParser(pydantic_object=EcommerceSupportResponse)
        response = FewShotsGenerator(few_shots=ECOMMERCE_SUPPORT_FEW_SHOTS,
                                     base_prompt=self.AGENT_INSTRUCTIONS,
                                     domain_data=domain_data,
                                     parser=parser,
                                     query=query,
                                     azure_open_ai_wrapper=self.azure_open_ai_wrapper,
                                     logger=self.logger).generate()

        self.logger.info(f"finished EcommerceSupportAgent with query: {query}")

        return response
