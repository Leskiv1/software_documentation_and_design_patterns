import requests

response = requests.post("http://127.0.0.1:8000/platform/load-csv")

print(f"Статус код: {response.status_code}")
print(f"Відповідь сервера: {response.json()}")