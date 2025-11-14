
from fastapi import APIRouter, Depends, Request, HTTPException
from app.schemas.ai import AdviceRequest, AdviceResponse
from app.services.ai_advisor import LocalAdvisor, ExternalAdvisor
from app.core.config import settings
from app.core.security import require_scope

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/advice", response_model=AdviceResponse)
def advice(req: AdviceRequest, request: Request):
    _ = require_scope(request, "verkoop:read")
    if settings.AI_ADVISOR_ENABLED:
        advisor = LocalAdvisor()
    else:
        advisor = ExternalAdvisor()
    return advisor.advise(req)
