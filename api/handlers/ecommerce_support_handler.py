from agents.ecommerce_support_agent.ecommerce_support_agent import EcommerceSupportAgent
from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from models.ecommerce_support_response_request import EcommerceSupportRequest
from utils.log_wrapper import LogWrapper


async def handle_ecommerce_support(g_request: EcommerceSupportRequest,
                                   logger: LogWrapper,
                                   azure_open_ai_wrapper: AzureOpenAIWrapper) -> dict:
    try:
        return EcommerceSupportAgent(
            logger,
            azure_open_ai_wrapper).run(g_request.query, g_request.domain_data)
    except Exception as e:
        logger.error("error while generating", tags={"g_request": g_request, "error": str(e)})
        raise e
