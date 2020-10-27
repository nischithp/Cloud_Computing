import requests
dictToSend = {"name": "Naveen"}
res = requests.post('http://127.0.0.1:8080/', json=dictToSend)
print(res.text)