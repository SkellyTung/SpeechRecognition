import json

data = {
    "name": "John Smith",
    "age": 35,
    "city": "New York"
}

with open("data.json", "w") as outfile:
    json.dump(data, outfile)
