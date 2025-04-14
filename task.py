from pydantic import BaseModel

class TaskModel(BaseModel):
    id: int
    name: str
    employee_id: int

    class Config:
        orm_mode = True