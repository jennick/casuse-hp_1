
from pydantic import BaseModel

class AdviceRequest(BaseModel):
    context: dict

class AdviceResponse(BaseModel):
    recommendations: list[str]
    rationale: str
