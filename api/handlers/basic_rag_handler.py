from langchain_community.vectorstores import FAISS

from agents.basic_rag_agent.basic_rag_agent import BasicRagAgent
from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from models.basic_llm_response import BasicLLMInput, BasicLLMOutput
from utils.log_wrapper import LogWrapper


async def handle_basic_rag(g_request: BasicLLMInput,
                           logger: LogWrapper,
                           vectorstore: FAISS,
                           azure_open_ai_wrapper: AzureOpenAIWrapper) -> BasicLLMOutput:
    try:
        llm_response = BasicRagAgent(logger,
                                     azure_open_ai_wrapper,
                                     vectorstore).run(g_request.query)
        return BasicLLMOutput(answer=llm_response)
    except Exception as e:
        logger.error("error while generating", tags={"g_request": g_request, "error": str(e)})
        raise e
