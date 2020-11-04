import requests
import json
dictToSend = {"data": {"email": "aaa@gmial.com",
                       "password": "*71237**123712383",
                       "username": "123",
                       "firstname": "123",
                       "lastname": "123"},
              "request": "login"}
#res = requests.post('https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/user_access', json=json.dumps(dictToSend))
print(isinstance(json.dumps(dictToSend), str))
res = requests.post('http://127.0.0.1:8080/', json=json.dumps(dictToSend))

print(res.text, res.status_code)