from pydantic import BaseModel

class ItemModel(BaseModel):
    id: int
    name: str
    count: int
    sold_since_restock: int

    class Config:
        orm_mode = True