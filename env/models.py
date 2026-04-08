from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    ticket_id: str
    customer_message: str
    history: Optional[str]

class Action(BaseModel):
    priority: str
    department: str
    response: str
