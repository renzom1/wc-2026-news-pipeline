import requests
import json

url = "https://newsapi.org/v2/everything"           #definimos el servicio que queremos usar de NewsAPI (se le llama endpoint)

params = {                                          #determinamos parametros que correspondan a las noticias del mundial
    "q": "World Cup 2026",                  
    "language": "en",
    "pageSize": 10,
    "apiKey": "662fe0534dae412f8700039bf16b10cc"    #apiKey seria nuestro "usuario" para pedirle cosas a la API
}

response = requests.get(url, params=params)                #enviamos la peticion

#print(response)

#print(response.json())
#print(response.json().keys())
#print (response.json()["articles"][0].keys())
#print(len(response.json()["articles"]))
#print(type(response.json()["articles"]))
#print(type(response.json()))
#articles = response.json()["articles"]
#print(len(articles))
"""
for article in articles:
    title = article["title"]
    description = article["description"]
    source = article["source"]["name"]
    url = article["url"]
    print(source)
"""

#print(response.json()["articles"][0])
#print(json.dumps(articles, indent=4))
#print(json.dumps(response.json()["articles"][1], indent=4))
#print(len(articles))
#print(json.dumps(response.json()["articles"][1]["source"]["name"]))
#print(type(response.json()["articles"][0]["source"]))
print(type(response.json()["articles"][0]["publishedAt"]))
print(type(response.json()["articles"][0]["url"]))