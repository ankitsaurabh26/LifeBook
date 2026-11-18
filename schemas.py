from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# We have created three different schemas because our API has three different responsibilities

class HabitCreate(BaseModel): # This defines what information the user must provide when creating a habit
    name: str # Pydantic checks: Is name a string? Yes/No
    description: Optional[str] = None


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class HabitOut(BaseModel): # This defines the structure of the response your API sends back to the frontend
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True} # setting allows Pydantic to read these values directly from your SQLAlchemy Habit object
