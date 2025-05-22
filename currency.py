import requests

response = requests.get("https://browser-info.ru/")

print(response.text)