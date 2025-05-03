from pydantic import BaseModel
from typing import Optional

class TaskModel(BaseModel):
    id: int
    name: str
    employee_id: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    employee_id: Optional[int] = None