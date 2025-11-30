from fastapi import Request
from typing import List


class UserContext:
    def __init__(self, sub: str, roles: List[str] | None = None, scopes: List[str] | None = None) -> None:
        self.sub = sub
        self.roles = roles or []
        self.scopes = scopes or []


def require_scope(request: Request, required: str) -> UserContext:
    """Very lightweight placeholder security.

    For now we don't enforce real auth in the verkoop-module.
    This function exists so the rest of the code can already depend
    on a future scope-based security model.

    In the future you can replace this with proper JWT validation that
    fills UserContext based on the Authorization header.
    """
    # TODO: integrate with Casuse-Core auth / JWT in a later phase.
    return UserContext(sub="dev-user", roles=["admin"], scopes=["*"])
