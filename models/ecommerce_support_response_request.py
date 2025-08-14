from pydantic import BaseModel, Field


class EcommerceSupportRequest(BaseModel):
    domain_data: str
    query: str


class EcommerceSupportResponse(BaseModel):
    response: str = Field(..., description="Answer to the customer query")
    action_required: bool = Field(..., description="True if human action is needed")