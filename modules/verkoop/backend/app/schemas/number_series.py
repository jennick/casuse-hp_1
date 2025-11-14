
from pydantic import BaseModel

class ReserveNumberRequest(BaseModel):
    series_name: str

class ReservedNumber(BaseModel):
    number: str
