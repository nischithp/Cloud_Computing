import requests
dictToSend = {"data": {"email": "naveen@gmial.com",
                       "password": "asodasnasidndai",
                       "username": "naveen",
                       "firstname": "nav",
                       "lastname": ""},
              "request": "register"}
#res = requests.post('https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/user_access', json=dictToSend)
res = requests.post('http://127.0.0.1:8080/', json=dictToSend)
print(res.text, res.status_code)