from pydantic import BaseModel
from typing import Optional

class ItemModel(BaseModel):
    id: int
    name: str
    count: int
    sold_since_restock: int

    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    count: Optional[int] = None
    sold_since_restock: Optional[int] = None