import requests

baseurl = "http://127.0.0.1:5000/"

# response = requests.post(baseurl + "video/3", {"likes": 12, "views": 10000, "name": "aman"})
# response = response.json()
# print(response)

response = requests.patch(baseurl + "video/3", {"name": "raj"})
response = response.json()
print(response)

response = requests.get(baseurl + "video/3")
response = response.json()

print(response)