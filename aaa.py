import requests

url = 'https://notify.eskiz.uz/api/auth/login'
body = dict(
    email = "ergashevazamera8@gmail.com",
    password = "tNps8gRc9GoxTic1vyc7sW0ucad6yZRMC28NpCxg"
)

responce = requests.post(url, data=body).json()
print(responce)