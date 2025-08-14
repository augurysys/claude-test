from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
from fastapi import Request


def get_azure_open_ai_wrapper_dependency(
        request: Request,
) -> AzureOpenAIWrapper:
    context = request.app.state.context
    return context.get("azure_open_ai_wrapper")
