import logging
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from ctx.app_context import AppContext
from api.bootstrap import create_app
from tests.mocks import mock_oauth_client, AzureOpenAIEmbeddingsMock
from utils.log_wrapper import LogWrapper
from utils.logger import get_logger

logger = LogWrapper(get_logger(name="Main", log_level=logging.INFO))


class AppTestClient(TestClient):
    def __init__(self, app):
        super().__init__(app)

    def request(self, method, url, **kwargs):
        headers = kwargs.pop("headers") or dict()
        headers["Authorization"] = "Bearer dummy"
        return super().request(method, url, headers=headers, **kwargs)


def create_app_context() -> AppContext:
    return (AppContext().
            set("logger", logger)
            .set("embeddings_client",
                 AzureOpenAIEmbeddingsMock(model="mock")).
            set("oauth_client", mock_oauth_client()))


ctx = create_app_context()
app = create_app(ctx=ctx)


def add_mock(dep, mock):
    app.dependency_overrides[dep] = mock


@pytest.fixture(scope="module")
def client() -> Generator:
    with AppTestClient(app) as client:
        yield client
        app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("OAUTH2_CLIENT_ID", "mock-id")
    monkeypatch.setenv("AUGURY_OAUTH2_INTERNAL_URL", "mock-id")
    monkeypatch.setenv("OAUTH2_CLIENT_SECRET", "mock-secret")
    monkeypatch.setenv("NSQD_TCP_ADDRESSES", "localhost:4150")
    monkeypatch.setenv("NSQD_HTTP_ADDRESSES", "localhost:4151")
    monkeypatch.setenv("LOOKUPD_HTTP_ADDRESSES", "localhost:4161")
    monkeypatch.setenv("MONGODB_URL", "mongodb://localhost:27017")
    monkeypatch.setenv("MONGODB_DB", "augury_development_test")
    print("NSQ consumer thread started")
