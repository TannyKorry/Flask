import requests
# # POST-запрос
# response = requests.post(
#     "http://127.0.0.1:5000/ads",
#     json={
#         "title": "asdf",
#         "text": "xfhchbjn",
#         "user": 'retyu'
#     })
# print(response.status_code)
# print(response.json())

# #GET-запрос

response = requests.get(
    "http://127.0.0.1:5000/ads/5",

)
# response = requests.delete(
#     "http://127.0.0.1:5000/ads/5",
#
# )
print(response.status_code)
print(response.json())
