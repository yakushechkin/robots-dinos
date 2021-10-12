import requests

BASE = "http://127.0.0.1:5000/"

data = [{"dim": 40}]

response = requests.post(BASE + "game/")
print(response.json())

response = requests.post(BASE + "game/", data[0])
print(response.json())

response = requests.get(BASE + "game/")
print(response.json())

# response = requests.post(BASE + "game/")
# print(response.json())
