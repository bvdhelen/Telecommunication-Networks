import json

data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian",
        "languages": ["hu", "en"],
        "tup": (1, 2, 25.5, True, False, None)
    }
}

print(json.dumps(data))
print("=====")

json_text = json.dumps(data)
print(json_text)
print("=====")
deser = json.loads(json_text)
print(deser)

print("=====")
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)

with open("data_file2.json", "w") as f:
    f.write(json_text)
    