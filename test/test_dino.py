# from main import create_space

# def test_create_space():
#     assert create_space().shape == (50, 50)

import requests

BASE = "http://127.0.0.1:5000/"

data = [{"x": 10, "y": 5}, {"x": 2, "y": 5}, {"x": 1, "y": 7}]


for i in range(len(data)):
    print(BASE + "dino/", data[i])
    response = requests.post(BASE + "dino/", data[i])
    print(response.json())

response = requests.get(BASE + "dino/", {"id": 6})
print(response.json())
