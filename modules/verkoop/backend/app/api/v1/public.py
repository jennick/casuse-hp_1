from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/ping")
def ping() -> dict:
    return {"status": "ok"}
