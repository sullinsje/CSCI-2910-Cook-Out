from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    availability = Column(String)

    def __repr__(self):
        return f"{self.id}\t{self.name}\t{self.availability}"
    
class Item(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    count = Column(Integer)
    sold_since_restock = Column(Integer)

    def __repr__(self):
        return f"{self.id}\t{self.name}\t{self.count}\t{self.sold_since_restock}"
    
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    employee_id = Column(Integer)

    def __repr__(self):
        return f"{self.id}\t{self.name}\t{self.employee_id}"