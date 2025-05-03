from pydantic import BaseModel
from typing import Optional

class EmployeeModel(BaseModel):
    id: int
    name: str
    availability: str

    class Config:
        orm_mode = True

class EmployeeUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    availability: Optional[str] = None