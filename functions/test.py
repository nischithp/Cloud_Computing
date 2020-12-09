import requests

# params = {"data": {"email": "a123aaa@gmial.com",
#                    "password": "71237**123712383",
#                    "username": "123",
#                    "firstname": "123",
#                    "lastname": "123"},
#           "request": "register"}

# dictToSend = {"data": {"email": "a123aaa@gmial.com",
#                        "password": "71237**123712383",
#                        "username": "123",
#                        "firstname": "123",
#                        "lastname": "123"},
#               "request": "login"}

# params = {
#     "userid": 7,
#     "video": {
#         "title": 'Music',
#         "url": "45-20201208010359.mp4",
#         "tag": "abcd",
#         "description": "asdasdas",
#         "privecy": "00000000000012"
#     }
# }
params = {"userid": 45}

res = requests.post('https://us-central1-cloudcomputinglab-291822.cloudfunctions.net/search', json=params)
# res = requests.post('http://127.0.0.1:8080/', json=params)

print(res.text, res.status_code)

# CREATE TABLE liked_videos (user_id INT(12) NOT NULL,video_id INT(14) NOT NULL,date_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,CONSTRAINT FK_lv_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT FK_lv_video_id FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE ON UPDATE CASCADE)

# CREATE TABLE videos (id INT(14) PRIMARY KEY AUTO_INCREMENT,title VARCHAR(1023) NOT NULL,URL VARCHAR(1023) NOT NULL,uploaded_by INT(12),views INT(11) NOT NULL DEFAULT 0,tags VARCHAR(511) DEFAULT NULL,description VARCHAR(511) DEFAULT NULL,privacy INT(2) NOT NULL DEFAULT 0,date_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,CONSTRAINT FK_userid FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE)

# CREATE TABLE users (id INT(12) PRIMARY KEY AUTO_INCREMENT,username VARCHAR(255) NOT NULL,firstname VARCHAR(255) NOT NULL,lastname VARCHAR(255),email VARCHAR(255) NOT NULL UNIQUE,password VARCHAR(255) NOT NULL,date_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP)
