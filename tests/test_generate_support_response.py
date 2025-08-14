from api.dependencies.azure_open_ai_wrapper import get_azure_open_ai_wrapper_dependency
from models.ecommerce_support_response_request import EcommerceSupportRequest
from tests.conftest import add_mock
from tests.mocks import AzureOpenAIWrapperMock


def test_health_check(client):
    response = client.get("/_ping")
    assert response.status_code == 200


def test_generate_support_response(client):
    add_mock(get_azure_open_ai_wrapper_dependency, AzureOpenAIWrapperMock)
    request = EcommerceSupportRequest(domain_data="hello", query="hello")
    # TODO replace with SDK call
    response = client.post("/examples/ecommerce_support", json=request.model_dump())
    assert response.status_code == 200
