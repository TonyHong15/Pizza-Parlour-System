import pip._vendor.requests as requests
import json
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "pizza")
print(response.json())
