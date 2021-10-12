# from main import create_space

# def test_create_space():
#     assert create_space().shape == (50, 50)

import requests

BASE = 'http://127.0.0.1:5000/'

data = [{'x': 10, 'y': 5},
        {'x': 1, 'y': 3},
        {'x': 7, 'y': 2}]


for i in range(len(data)):
    print(BASE + "dino/{}".format(str(i)), data[i])
    response = requests.put(BASE + "dino/{}".format(str(i)), data[i])
    print(response.json())

response = requests.get(BASE + "dino/2")
print(response.json())

