from typing import Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: Optional[int] = Field(default=0)
    title: str
    description: str
    is_done: bool
