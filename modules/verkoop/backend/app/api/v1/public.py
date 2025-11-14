
from fastapi import APIRouter
router = APIRouter(prefix="/public", tags=["public"])

@router.get("/seller_card/{seller_code}")
def seller_card(seller_code: str):
    # minimal public card
    return {"code": seller_code, "name": "Seller "+seller_code, "rating": 4.8}
