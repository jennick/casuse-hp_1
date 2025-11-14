
from fastapi import HTTPException, status, Request
from typing import List, Optional
import base64, json

class UserContext:
    def __init__(self, sub: str, roles: List[str], scopes: List[str]):
        self.sub = sub
        self.roles = roles
        self.scopes = scopes

def parse_bearer_token(token: str) -> UserContext:
    # Extremely simplified parser (expects header.payload.signature; decodes payload as base64url JSON)
    try:
        parts = token.split(".")
        if len(parts) < 2:
            raise ValueError("bad token")
        payload_b64 = parts[1] + "=="  # pad
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode("utf-8")).decode("utf-8"))
        roles = payload.get("roles", [])
        scopes = payload.get("scopes", [])
        sub = payload.get("sub", "anonymous")
        return UserContext(sub=sub, roles=roles, scopes=scopes)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def require_scope(request: Request, required: str):
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    ctx = parse_bearer_token(auth.removeprefix("Bearer "))
    if required not in ctx.scopes and required not in ctx.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing scope {required}")
    return ctx
