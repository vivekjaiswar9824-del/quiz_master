import requests

url = "http://127.0.0.1:8000/api/quizzes/"
data = {"title": "Sample Quiz"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
