from employee import EmployeeModel
import requests

base_url = "http://localhost:8000"

print(requests.get(f"{base_url}/employees/", params={'name': 'Alice Johnson'}).content)
print(requests.get(f"{base_url}/employees/{1}").content)