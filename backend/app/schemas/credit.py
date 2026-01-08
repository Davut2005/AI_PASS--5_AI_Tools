from pydantic import BaseModel
from datetime import datetime

class CreditResponse(BaseModel):
    balance: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CreditTransactionResponse(BaseModel):
    id: int
    amount: int
    type: str
    description: str
    created_at: datetime
    
    class Config:
        from_attributes = True