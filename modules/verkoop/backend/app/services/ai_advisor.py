
from app.schemas.ai import AdviceRequest, AdviceResponse

class LocalAdvisor:
    def advise(self, req: AdviceRequest) -> AdviceResponse:
        ctx = req.context or {}
        recommendations = []
        if ctx.get("customer_segment") == "enterprise":
            recommendations.append("Offer volume discount and extended warranty.")
        if ctx.get("region") == "North":
            recommendations.append("Prioritize delivery slots due to logistics load in North.")
        if not recommendations:
            recommendations.append("Propose bundle: Widget A + Service C.")
        rationale = "Rule-based heuristics without external calls; no PII leaves the system."
        return AdviceResponse(recommendations=recommendations, rationale=rationale)

class ExternalAdvisor:
    # stub only
    def advise(self, req: AdviceRequest) -> AdviceResponse:
        return AdviceResponse(recommendations=["External provider not configured"], rationale="Stub")
