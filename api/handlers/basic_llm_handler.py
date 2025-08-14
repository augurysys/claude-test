from agents.basic_llm_agent.basic_llm_agent import BasicLlmAgent
from core.llms.azure_open_ai_wrapper import get_default_azure_open_ai_wrapper
from models.basic_llm_response import BasicLLMInput, BasicLLMOutput
from utils.log_wrapper import LogWrapper


async def handle_basic_llm(g_request: BasicLLMInput,
                           logger: LogWrapper) -> BasicLLMOutput:
    try:
        llm_response = BasicLlmAgent(logger, get_default_azure_open_ai_wrapper(logger)).run(g_request.query)
        return BasicLLMOutput(answer=llm_response)
    except Exception as e:
        logger.error("error while generating", tags={"g_request": g_request, "error": str(e)})
        raise e
