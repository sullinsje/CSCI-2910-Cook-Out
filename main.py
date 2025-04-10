from fastapi import FastAPI, HTTPException, Query
from employee import EmployeeModel
from item import ItemModel
from task import TaskModel
from data_models import Base, Employee, Item, Task

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./social_media.db"
engine = create_engine(DB_URL)
Base.metadata.create_all(bind=engine)
session_factory = sessionmaker(bind=engine)
session = session_factory()

app = FastAPI()

#region Employee endpoints

#get_employees,                 endpoint:   /employees/
#create_employee,               endpoint:   /employees/
#get_employee,                  endpoint:   /employees/{id}
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