from pydantic import BaseModel, Field


class BasicLLMInput(BaseModel):
    query: str


class BasicLLMOutput(BaseModel):
    answer: str = Field(..., description="Answer to the customer query")
