from typing import Dict, Any

class AIAgentService:
    def explain_routes(self) -> Dict[str, Any]:
        return {
            "title": "Beschikbare routes",
            "steps": [
                "GET /healthz",
                "GET /readyz",
                "POST /auth/login",
                "GET /auth/me",
                "POST /auth/refresh",
                "POST /auth/2fa/setup",
                "POST /auth/2fa/verify",
                "GET /modules",
                "POST /ai/ask"
            ]
        }

    def how_to_add_module(self) -> Dict[str, Any]:
        return {
            "title": "Module toevoegen",
            "steps": [
                "Nieuwe module in ./modules/<naam>/",
                "Voeg db, backend, frontend toe in docker-compose.yml",
                "Zet JWT check in module-backend",
                "Voeg module toe aan /modules endpoint"
            ]
        }

    def debug_hints(self) -> Dict[str, Any]:
        return {
            "title": "Debug login / modules",
            "steps": [
                "Check core-db",
                "Check alembic upgrade",
                "Check JWT_SECRET in core en modules",
                "docker compose logs core-backend --tail=200"
            ]
        }

    def answer(self, question: str) -> Dict[str, Any]:
        q = question.lower()
        if "endpoint" in q or "route" in q:
            return self.explain_routes()
        if "module" in q:
            return self.how_to_add_module()
        if "debug" in q or "login" in q:
            return self.debug_hints()
        return {"title": "Onbekend", "steps": ["Stel je vraag concreter."]}
