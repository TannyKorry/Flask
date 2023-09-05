import requests
#POST-запрос
response = requests.post(
    "http://127.0.0.1:5000/ads/",
    json={"title": "Продам шкаф", "text": "123", "user": "Cергей"},
)
print(response.status_code)
print(response.json())



#GET-запрос
response = requests.get(
    "http://127.0.0.1:5000/ads/1",

)
print(response.status_code)
print(response.json())
