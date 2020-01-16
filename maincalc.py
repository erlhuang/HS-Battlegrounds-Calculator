import requests

url = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards/sets/Battlegrounds"
data = {}
querystring = {"cost":"2"}

headers = {
    'x-rapidapi-host': "omgvamp-hearthstone-v1.p.rapidapi.com",
    'x-rapidapi-key': "dce5f008a7msh663c93cb6f5940ap102dbejsn84c97939d703"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
