from pydantic import BaseModel

class ScheduleModel(BaseModel):
    """
    Pydantic model representing a single schedule entry for an employee
    """
    day: str            # e.g. "Monday"
    employee_id: int
    name: str
    start_time: str     # "HH:MM"
    end_time: str       # "HH:MM"

    class Config:
        orm_mode = True
