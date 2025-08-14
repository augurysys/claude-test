import logging
import os
from auth_sdk.init import init_oauth_client
from raven import Client as RavenClient

from ctx.app_context import AppContext
from langchain_openai import AzureOpenAIEmbeddings

from core.llms.azure_open_ai_wrapper import get_default_azure_open_ai_wrapper
from utils.log_wrapper import LogWrapper
from utils.logger import get_logger
from py_wrapper_mongo import Client

default_embedding_model = "text-embedding-ada-002"


def get_default_context() -> AppContext:
    logger = LogWrapper(get_logger(name="Main", log_level=logging.INFO), RavenClient())
    return (AppContext().set("logger", logger)
            .set("db", Client(os.environ.get("MONGODB_URL", None)).get_database(os.environ.get("MONGODB_DB", None)))
            .set("embeddings_client", AzureOpenAIEmbeddings(model=default_embedding_model))
            .set("azure_open_ai_wrapper", get_default_azure_open_ai_wrapper(logger)))
