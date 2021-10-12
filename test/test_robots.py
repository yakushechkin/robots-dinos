# from main import create_space

# def test_create_space():
#     assert create_space().shape == (50, 50)

import requests

BASE = 'http://127.0.0.1:5000/'

data = [{'x': 10, 'y': 5, 'direction': 'east'},
        {'x': 2, 'y': 6, 'direction': 'west'},
        {'x': 7, 'y': 2, 'direction': 'east'}]


for i in range(len(data)):
    print(BASE + "robot/{}".format(str(i)), data[i])
    response = requests.put(BASE + "robot/{}".format(str(i)), data[i])
    print(response.json())

response = requests.get(BASE + "robot/2")
print(response.json())

# response = requests.patch(BASE + "robot/2", {"name": "Old name", "likes": 1234, "views": 13})
# print(response.json())

