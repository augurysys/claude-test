from unittest.mock import MagicMock
from auth_sdk.dto import ValidateTokenResponse, ValidateTokenClient

from models.ecommerce_support_response_request import EcommerceSupportResponse


class AzureOpenAIEmbeddingsMock:
    def __init__(self, model):
        self.model = model

    def embed_query(self, query: str) -> list:
        return [0.1, 0.2, 0.3]

    def embed_documents(self, documents: list) -> list:
        return [[0.1, 0.2, 0.3] for _ in documents]


class AzureOpenAIWrapperMock:
    def invoke(self, prompt):
        class MockResponse:
            def __init__(self, content):
                self.content = content
                self.id = "mock-id"
        
        return MockResponse(EcommerceSupportResponse(response="mocked_response", action_required=True).model_dump_json())


# TODO move this to the SDK
def mock_oauth_client():
    mock = MagicMock()
    mock.validate_token.return_value = ValidateTokenResponse(
        scopes=["augury", "user"],
        client=ValidateTokenClient(name="mock_client", id="mock_client_id"),
        userData=None
    ).to_dict()

    return mock
