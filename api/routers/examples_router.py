from fastapi import APIRouter, HTTPException, Depends
from fastapi import Request
from langchain_community.vectorstores import FAISS

from api.dependencies.azure_open_ai_wrapper import get_azure_open_ai_wrapper_dependency
from api.dependencies.logger import get_request_logger
from api.dependencies.vector_store import get_vector_store_dependency
from api.handlers.basic_llm_handler import handle_basic_llm
from api.handlers.basic_rag_handler import handle_basic_rag
from api.handlers.book_recommender_handler import handle_book_recommender
from api.handlers.ecommerce_support_handler import handle_ecommerce_support
from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper

from models.basic_llm_response import BasicLLMOutput, BasicLLMInput
from models.ecommerce_support_response_request import EcommerceSupportResponse, EcommerceSupportRequest
from utils.log_wrapper import LogWrapper

router = APIRouter(prefix="/examples", tags=["examples"])


@router.post("/basic_llm", response_model=BasicLLMOutput)
async def basic_llm(request: Request,
                    g_request: BasicLLMInput,
                    logger: LogWrapper = Depends(get_request_logger)):
    try:
        tags = {}
        logger.info("started basic_llm", tags=tags)
        result = await handle_basic_llm(g_request, logger)
        logger.info("completed basic_llm", tags=tags)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/basic_rag", response_model=BasicLLMOutput)
async def basic_rag(request: Request,
                    g_request: BasicLLMInput,
                    logger: LogWrapper = Depends(get_request_logger),
                    azure_open_ai_wrapper: AzureOpenAIWrapper = Depends(get_azure_open_ai_wrapper_dependency),
                    vector_store: FAISS = Depends(get_vector_store_dependency)):
    try:
        tags = {}
        logger.info("started basic_rag", tags=tags)
        result = await handle_basic_rag(g_request,
                                        logger,
                                        vector_store,
                                        azure_open_ai_wrapper)
        logger.info("completed basic_rag", tags=tags)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/books", response_model=BasicLLMOutput)
async def books_recommender(request: Request,
                            g_request: BasicLLMInput,
                            logger: LogWrapper = Depends(get_request_logger),
                            azure_open_ai_wrapper: AzureOpenAIWrapper = Depends(get_azure_open_ai_wrapper_dependency),
                            vector_store: FAISS = Depends(get_vector_store_dependency)):
    try:
        tags = {}
        logger.info("started books_recommender", tags=tags)
        result = await handle_book_recommender(g_request,
                                               logger,
                                               vector_store,
                                               azure_open_ai_wrapper)
        logger.info("completed books_recommender", tags=tags)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ecommerce_support", response_model=EcommerceSupportResponse)
async def ecommerce_support(request: Request,
                            g_request: EcommerceSupportRequest,
                            logger: LogWrapper = Depends(get_request_logger),
                            azure_open_ai_wrapper: AzureOpenAIWrapper = Depends(get_azure_open_ai_wrapper_dependency)):
    """
    Generate support response
    """
    try:
        tags = {}
        logger.info("started router support response", tags=tags)
        result = await handle_ecommerce_support(g_request, logger, azure_open_ai_wrapper=azure_open_ai_wrapper)
        logger.info("completed router support response", tags=tags)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))