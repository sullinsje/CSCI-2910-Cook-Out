from employee import EmployeeModel
import requests

base_url = "http://localhost:8000"

print(requests.get(f"{base_url}/employees/", params={'name': 'Alice Johnson'}).content)
print(requests.get(f"{base_url}/employees/{1}").content)

print(requests.get(f"{base_url}/items/", params={'name': 'Apple iPhone 14'}).content)
print(requests.get(f"{base_url}/items/{1}").content)

print(requests.get(f"{base_url}/tasks/", params={'name': 'Stock new phone models'}).content)
print(requests.get(f"{base_url}/tasks/{1}").content)