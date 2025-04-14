from fastapi import FastAPI, HTTPException, Query
from employee import EmployeeModel
from item import ItemModel
from task import TaskModel
from data_models import Base, Employee, Item, Task
from typing import List

from sqlalchemy import create_engine, select, desc
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
            employee = session.query(Employee).all()
    except:
        raise HTTPException(404, "Item not found")
    
    return employee

#create_employee,               endpoint:   /employees/
@app.post("/employees/", response_model=EmployeeModel)
def create_employee(employee: EmployeeModel):
    uniqueId = session.query(Employee).order_by(desc(Employee.id)).first().id
    uniqueId += 1
    db_employee = Employee(
        id=uniqueId, 
        name=employee.name, 
        availability=employee.availability
    )
    
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)  

    return db_employee  

#get_employee,                  endpoint:   /employees/{id}
@app.get("/employees/{id}", response_model=EmployeeModel)
async def get_employee(id: int):
    try:
        employee = session.query(Employee).filter(Employee.id == id).one()
    except:
        raise HTTPException(404, "Item not found")
    
    return employee

#update_employee,               endpoint:   /employees/{id}
@app.put("/employees/{id}", response_model=EmployeeModel)
async def update_employee(id: int, employee: EmployeeModel):
    try:
        db_employee = session.query(Employee).filter(Employee.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_employee.name = employee.name
    db_employee.availability = employee.availability

    try:
        session.commit()
        session.refresh(db_employee)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_employee

#delete_employee,               endpoint:   /employees/{id}
@app.put("/employees/{id}", response_model=EmployeeModel)
async def delete_employee(id: int):
    try:
        db_employee = session.query(Employee).filter(Employee.id == id).one()
        db_employee_tasks = session.query(Task).filter(Task.employee_id == id).one()
    except:
        raise HTTPException(404, "Item not found")
    
    try:
        session.delete(db_employee)
        session.delete(db_employee_tasks)
        session.commit()
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_employee

#patch_employee_name,           endpoint:   /employees/{id}
@app.put("/employees/{id}", response_model=EmployeeModel)
async def patch_employee_name(id: int, name: str):
    try:
        db_employee = session.query(Employee).filter(Employee.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_employee.name = name

    try:
        session.commit()
        session.refresh(db_employee)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_employee

#patch_employee_availability    endpoint:   /employees/{id}
@app.put("/employees/{id}", response_model=EmployeeModel)
async def patch_employee_availability(id: int, availability: str):
    try:
        db_employee = session.query(Employee).filter(Employee.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_employee.availability = availability
    
    try:
        session.commit()
        session.refresh(db_employee)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_employee

#endregion

#region Inventory endpoints
@app.get("/items/", response_model=List[ItemModel])
async def get_items(name: str = Query(default=None, alias="name")):
    try:
        if name:
            item = session.query(Item).filter(Item.name == name).all()
        else:
            item = session.query(Item).all()
    except:
        raise HTTPException(404, "Item not found")
    
    return item

@app.post("/items/", response_model=ItemModel)
def create_item(item: ItemModel):
    uniqueId = session.query(Item).order_by(desc(Item.id)).first().id
    uniqueId += 1
    db_item = Item(
        id=uniqueId, 
        name=item.name, 
        count=item.count,
        sold_since_restock=item.sold_since_restock
    )
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)  

    return db_item  

@app.get("/items/{id}", response_model=ItemModel)
async def get_item(id: int):
    try:
        item = session.query(Item).filter(Item.id == id).one()
    except:
        raise HTTPException(404, "Item not found")
    
    return item

@app.put("/items/{id}", response_model=ItemModel)
async def update_item(id: int, item: ItemModel):
    try:
        db_item = session.query(Item).filter(Item.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_item.name = item.name
    db_item.count = item.count
    db_item.sold_since_restock = item.sold_since_restock

    try:
        session.commit()
        session.refresh(db_item)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_item

@app.put("/items/{id}", response_model=ItemModel)
async def delete_item(id: int):
    try:
        db_item = session.query(Item).filter(Item.id == id).one()
    except:
        raise HTTPException(404, "Item not found")
    
    try:
        session.delete(db_item)
        session.commit()
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_item

@app.put("/items/{id}", response_model=ItemModel)
async def patch_item_name(id: int, name: str):
    try:
        db_item = session.query(Item).filter(Item.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_item.name = name

    try:
        session.commit()
        session.refresh(db_item)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_item

@app.put("/items/{id}", response_model=ItemModel)
async def patch_item_count(id: int, count: str):
    try:
        db_item = session.query(Item).filter(Item.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_item.count = count
    
    try:
        session.commit()
        session.refresh(db_item)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_item

@app.put("/items/{id}", response_model=ItemModel)
async def patch_item_sold_since_restock(id: int, sold_since_restock: str):
    try:
        db_item = session.query(Item).filter(Item.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_item.sold_since_restock = sold_since_restock
    
    try:
        session.commit()
        session.refresh(db_item)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_item

#endregion

#region Task endpoints

@app.get("/tasks/", response_model=List[TaskModel])
async def get_tasks(name: str = Query(default=None, alias="name")):
    try:
        if name:
            task = session.query(Task).filter(Task.name == name).all()
        else:task = session.query(Task).all()
    except:
        raise HTTPException(404, "Item not found")
    
    return task

@app.post("/tasks/", response_model=TaskModel)
def create_task(task: TaskModel):
    uniqueId = session.query(Task).order_by(desc(Task.id)).first().id
    uniqueId += 1
    db_task = Task(
        id=uniqueId, 
        name=task.name, 
        employee_id=task.employee_id
    )
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)  

    return db_task  

@app.get("/tasks/{id}", response_model=TaskModel)
async def get_task(id: int):
    try:
        task = session.query(Task).filter(Task.id == id).one()
    except:
        raise HTTPException(404, "Item not found")
    
    return task

@app.put("/tasks/{id}", response_model=TaskModel)
async def update_task(id: int, task: TaskModel):
    try:
        db_task = session.query(Task).filter(Task.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_task.name = task.name
    db_task.employee_id = task.employee_id

    try:
        session.commit()
        session.refresh(db_task)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_task

@app.put("/tasks/{id}", response_model=TaskModel)
async def delete_task(id: int):
    try:
        db_task = session.query(Task).filter(Task.id == id).one()
    except:
        raise HTTPException(404, "Item not found")
    
    try:
        session.delete(db_task)
        session.commit()
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_task

@app.put("/tasks/{id}", response_model=TaskModel)
async def patch_task_name(id: int, name: str):
    try:
        db_task = session.query(Task).filter(Task.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_task.name = name

    try:
        session.commit()
        session.refresh(db_task)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_task

@app.put("/tasks/{id}", response_model=TaskModel)
async def patch_task_employee_id(id: int, employee_id: int):
    try:
        db_task = session.query(Task).filter(Task.id == id).one()
    except:
        raise HTTPException(404, "Item not found")

    db_task.employee_id = employee_id
    
    try:
        session.commit()
        session.refresh(db_task)
    except:
        raise HTTPException(500, "Internal Server Error")
    
    return db_task

#endregion