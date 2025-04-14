from fastapi import FastAPI, HTTPException, Query
from employee import EmployeeModel
from item import ItemModel
from task import TaskModel
from data_models import Base, Employee, Item, Task
from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./data.db"
engine = create_engine(DB_URL)
Base.metadata.create_all(bind=engine)
session_factory = sessionmaker(bind=engine)
session = session_factory()

app = FastAPI()

#region Employee endpoints

#get_employees,                 endpoint:   /employees/
@app.get("/employees/", response_model=List[EmployeeModel])
async def get_employees(name: str = Query(default=None, alias="name")):
    # If a name is provided, filter users by the name
    try:
        if name:
            employee = session.query(Employee).filter(Employee.name == name).all()
        else:
            user = session.query(Employee).all()
    except:
        raise HTTPException(404, "Item not found")
    
    return employee

#create_employee,               endpoint:   /employees/

#get_employee,                  endpoint:   /employees/{id}
@app.get("/employees/{id}", response_model=EmployeeModel)
async def get_employees(id: int):
    try:
        employee = session.query(Employee).filter(Employee.id == id).one()
    except:
        raise HTTPException(404, "Item not found")
    
    return employee

#update_employee,               endpoint:   /employees/{id}
#delete_employee,               endpoint:   /employees/{id}
#patch_employee_name,           endpoint:   /employees/{id}
#patch_employee_availability    endpoint:   /employees/{id}
#endregion

#region Inventory endpoints

#get_items,                     endpoint:   /items/
#create_item,                   endpoint:   /items/
#get_item,                      endpoint:   /items/{id}
#update_item,                   endpoint:   /items/{id}
#delete_item,                   endpoint:   /items/{id}
#patch_item_name,               endpoint:   /items/{id}
#patch_item_count               endpoint:   /items/{id}
#patch_item_sold_since_restock  endpoint:   /items/{id}

#endregion

#region Task endpoints

#get_tasks,                 endpoint:   /tasks/
#create_task,               endpoint:   /tasks/
#get_task,                  endpoint:   /tasks/{id}
#update_task,               endpoint:   /tasks/{id}
#delete_task,               endpoint:   /tasks/{id}
#patch_task_name,           endpoint:   /tasks/{id}
#patch_task_employee_id     endpoint:   /tasks/{id}

#endregion