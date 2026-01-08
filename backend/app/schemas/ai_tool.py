from pydantic import BaseModel
from typing import Optional

class AIToolRequest(BaseModel):
    tool_name: str
    input_text: str
    
class AIToolResponse(BaseModel):
    output_text: str
    credits_used: int
    remaining_credits: int