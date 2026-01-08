from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrganizationCreate(BaseModel):
    name: str

class OrganizationResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    subscription_tier: str
    credits: int
    created_at: datetime
    
    class Config:
        from_attributes = True