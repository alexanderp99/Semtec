
import requests
from hidden.old import AddPersonRequest

person = AddPersonRequest(name="New Alex", target="e0")
response = requests.post(url="http://localhost:8000/add_person", json=person.dict())
print(response.json())