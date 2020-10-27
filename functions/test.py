import requests
dictToSend = {"name": "Naveen"}
#res = requests.post('https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/user_access', json=dictToSend)
res = requests.post('http://127.0.0.1:8080/', json=dictToSend)
print(res.text)