import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable
import logging
import pathlib
from contextlib import asynccontextmanager
import uvicorn
from raven import Client as RavenClient

from ctx.app_context import AppContext
from api.bootstrap import create_app

from fastapi import FastAPI

from ctx.context import get_default_context
from utils.log_wrapper import LogWrapper
from utils.logger import get_logger

logger = LogWrapper(get_logger(name="Main", log_level=logging.INFO), RavenClient())
root_dir = pathlib.Path(__file__).parent.parent.resolve()


@asynccontextmanager
async def lifespan_main(_app: FastAPI):
    # Set up OpenTelemetry tracing
    #setup_telemetry(_app)

    async with lifespan_gen_ai(_app):
        yield

# example vector store usage
# .set("book_recommendation_faiss",
#     default_faiss_vector_store_wrapper(
#         logger=logger,
#         index_path=str(root_dir / "agents" / "book_recommender" / "faiss_index"),
#         dataset_path=str(root_dir / "agents" / "book_recommender" / "dataset")
#     )))


@asynccontextmanager
async def lifespan_gen_ai(_app: FastAPI):
    try:
        _app.state.example_state_variable = "example_state_variable"
    except Exception as e:
        logger.error("error while starting app", tags={"error": str(e)})
        raise e

    yield


def get_app(ctx: AppContext):
    return create_app(lifespan_main=lifespan_main, ctx=ctx)

ctx = get_default_context()
app = get_app(ctx=ctx)

if __name__ == '__main__':
    logger.info("Starting.")
    uvicorn.run(app, port=3000, host='0.0.0.0')
    logger.info("Exiting.")

