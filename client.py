from employee import EmployeeModel, EmployeeUpdate
from item import ItemModel, ItemUpdate
from task import TaskModel, TaskUpdate
import requests

base_url = "http://localhost:8000"

def get_tests():
    print(requests.get(f"{base_url}/employees/", params={'name': 'Alice Johnson'}).content)
    print(requests.get(f"{base_url}/employees/{1}").content)

    print(requests.get(f"{base_url}/items/", params={'name': 'Apple iPhone 14'}).content)
    print(requests.get(f"{base_url}/items/{1}").content)

    print(requests.get(f"{base_url}/tasks/", params={'name': 'Stock new phone models'}).content)
    print(requests.get(f"{base_url}/tasks/{1}").content)

def update_emp_tests():
    emp = EmployeeModel(id=1, name="Alex John", availability="10:00 - 18:00")
    print(requests.put(f"{base_url}/employees/{1}", emp.model_dump_json()))

    up = EmployeeUpdate(name="John Smith")
    print(requests.patch(f"{base_url}/employees/{2}", up.model_dump_json(exclude_unset=True)))

def update_item_tests():
    item = ItemModel(id=1, name="iPhone 14", count=10, sold_since_restock=0)
    item2 = ItemUpdate(count=12)
    print(requests.patch(f"{base_url}/items/{1}", item2.model_dump_json(exclude_unset=True)))
    print(requests.put(f"{base_url}/items/{2}", item.model_dump_json()))

def update_task_tests():
    task = TaskModel(id=1, name="clean", employee_id=1)
    task2 = TaskUpdate(employee_id=2)
    print(requests.patch(f"{base_url}/tasks/{1}", task2.model_dump_json(exclude_unset=True)))
    print(requests.put(f"{base_url}/tasks/{2}", task.model_dump_json()))

def delete_tests():
    print(requests.delete(f"{base_url}/tasks/{14}"))
    print(requests.delete(f"{base_url}/items/{30}"))
    print(requests.delete(f"{base_url}/employees/{12}"))

def post_tests():
        emp = EmployeeModel(id=1, name="Alex John", availability="10:00 - 18:00")
        print(requests.post(f"{base_url}/employees/", emp.model_dump_json()))

        item = ItemModel(id=1, name="iPhone 14", count=10, sold_since_restock=0)
        print(requests.post(f"{base_url}/items/", item.model_dump_json()))

        task = TaskModel(id=1, name="clean", employee_id=1)
        print(requests.post(f"{base_url}/tasks/", task.model_dump_json()))


post_tests()

