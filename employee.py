from pydantic import BaseModel

class EmployeeModel(BaseModel):
    id: int
    name: str
    availability: str

    class Config:
        orm_mode = True