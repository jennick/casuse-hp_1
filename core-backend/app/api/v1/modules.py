from fastapi import APIRouter

router = APIRouter(prefix="/modules", tags=["modules"])

MODULES = [
    {"key": "verkoop", "name": "Verkoop", "url": "http://localhost:20040", "status": "online"},
    {"key": "website", "name": "Website", "url": "http://localhost:20060", "status": "online"},
    {"key": "inventaries", "name": "Inventaries", "url": "http://localhost:20080", "status": "online"},
    {"key": "facturatie", "name": "Facturatie", "url": "http://localhost:20110", "status": "online"},
    {"key": "magazijn", "name": "Magazijn", "url": "http://localhost:20130", "status": "online"},
    {"key": "productie", "name": "Productie", "url": "http://localhost:20150", "status": "online"},
    {"key": "overzicht-modules", "name": "Overzicht modules", "url": "http://localhost:20162", "status": "online"}
]

@router.get("")
def list_modules():
    return MODULES
