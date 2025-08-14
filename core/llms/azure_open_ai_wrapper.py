from langchain_openai import AzureChatOpenAI
from langchain_community.callbacks import get_openai_callback
from typing import Optional
import warnings
from utils.log_wrapper import LogWrapper

class AzureOpenAIWrapper(AzureChatOpenAI):
    """Wrapper for Azure OpenAI models with token logging and tracing functionality.
    
    This class extends AzureChatOpenAI to provide enhanced functionality with token usage tracking
    and structured logging capabilities.
    
    Args:
        api_version (str): Azure OpenAI API version.
        azure_deployment (str): Azure OpenAI deployment name.
        temperature (float): Temperature setting for the model (0-1).
        max_tokens (int): Maximum number of tokens to generate.
        timeout (Optional[int], optional): Request timeout in seconds. Defaults to None.
        max_retries (int, optional): Maximum number of retries for API calls. Defaults to 2.
        logger (Optional[LogWrapper], optional): Logger instance for tracking token usage. Defaults to None.
    
    Attributes:
        logger: Logger for tracking token usage and costs.
    
    Examples:
        ```
        from utils.log_wrapper import LogWrapper
        from core.llms.azure_open_ai_wrapper import AzureOpenAIWrapper
        from core.langsmith.tracing import enable_tracing
        
        # Optional: Enable tracing
        enable_tracing("my-project")
        
        logger = LogWrapper(__name__)
        
        # Create a custom model
        model = AzureOpenAIWrapper(
            api_version="2024-08-01-preview",
            azure_deployment="gpt-4o",
            temperature=0.7,
            max_tokens=2000,
            logger=logger
        )
        
        # Use the model
        response = model.invoke("Tell me about AI")
        ```
    """
    logger: Optional[LogWrapper] = None
    
    def __init__(self, 
                 api_version: str,
                 azure_deployment: str, 
                 temperature: float,
                 max_tokens: int,
                 timeout: Optional[int] = None,
                 max_retries: int = 2,
                 logger: Optional[LogWrapper] = None, 
                 **kwargs):
        # Initialize the parent class first
        super().__init__(
            api_version=api_version,
            azure_deployment=azure_deployment,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs
        )
        
        # Assign to private attributes
        self.logger = logger
        
        if not logger:
            warnings.warn("No logger provided, token logging will not be enabled")

    def _log_structured(self, tokens_used, run_id, total_cost):
        """Log structured information about the LLM run in a format parsable by log systems.
        
        Args:
            tokens_used: Number of tokens used in the request
            run_id: Unique identifier for the run
            total_cost: Total cost of the request
        """
        if self.logger:
            self.logger.info(f"[run_id={run_id}] [tokens_used={tokens_used}] [total_cost={total_cost}]")
    
    def invoke(self, *args, **kwargs):
        with get_openai_callback() as cb:
            result = super().invoke(*args, **kwargs)
            run_id = result.id
            self._log_structured(cb.total_tokens, run_id, cb.total_cost)
        return result
        
    async def ainvoke(self, *args, **kwargs):
        with get_openai_callback() as cb:
            result = await super().ainvoke(*args, **kwargs)
            run_id = result.id
            self._log_structured(cb.total_tokens, run_id, cb.total_cost)
        return result


def get_default_azure_open_ai_wrapper(logger: LogWrapper) -> AzureOpenAIWrapper:
    """Creates an AzureOpenAIWrapper with standard configuration.
    
    This is a convenience function that creates an AzureOpenAIWrapper instance with
    commonly used default settings for the Azure OpenAI service.
    
    Args:
        logger (LogWrapper): Logger instance for tracking token usage.
    
    Returns:
        AzureOpenAIWrapper: A configured wrapper for Azure OpenAI with default settings.
    
    Examples:
        ```
        from utils.log_wrapper import LogWrapper
        
        logger = LogWrapper(__name__)
        model = get_default_azure_open_ai_wrapper(logger)
        response = model.invoke("Hello!")
        ```
    """
    return AzureOpenAIWrapper(
        api_version="2024-08-01-preview",
        azure_deployment="gpt-4o",
        temperature=0,
        max_tokens=1000,
        timeout=None,
        max_retries=2,
        logger=logger
    )
