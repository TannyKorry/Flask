import requests
# POST-запрос
response = requests.post(
    "http://127.0.0.1:5000/ads",
    json={
        "title": "Продам сервиз",
        "text": "В отличном состоянии",
        "user": 'Светлана'
    })

# GET-запрос
response = requests.get(
    "http://127.0.0.1:5000/ads/8",
)

# DELETE-запрос
response = requests.delete(
    "http://127.0.0.1:5000/ads/8",
)

print(response.status_code)
print(response.json())
