import json
import requests

with open("./info.txt") as file:
    lines = file.readlines()

session = requests.session()

api = "bearer " + lines[7][:-1]

keys = {
    "Authorization":api,
    "Content-Type":"application/json"
}

session.headers.update(keys)

url = "https://api.tcgplayer.com/v1.39.0/catalog/categories/1/search"
page = session.get(url)

body = {
    "limit":10000,
    "filters":[ { "name": "ProductName", "values": [ "Swamp" ] } ]
}

#thing = requests.post(api).text
thing = session.post(url, json=body).text

array = json.loads(thing)

for id in array['results']:
    print(id)
