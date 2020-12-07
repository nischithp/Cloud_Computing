
from google.cloud import storage
import sqlalchemy
from flask import jsonify
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import json
import datetime
import os

'''
Called by HTTP request,
input JSON: Contains userid and information about video uploaded
    {   "userid": 7,
        "video": {
            "title" : 'cat',
            "url": 1,
            "tag": "abcd",              (optional)
            "description": "asdasdas",  (optional)
            "privecy": "00000000000012" (optional)
        }
    }
Enters user video details in SQL database and creates video thumbnail.
'''

def upload(request):

    error = {"bad request": {"status": "fail", "status_code": 400,
                             "error": "No JSON, request should include JSON object"},
             "unauthorised": {"status": "fail", "status_code": 401,
                              "error": "Incorrect password, please enter correct password"},
             "forbidden": {"status": "fail", "status_code": 403,
                           "error": "user doesn't exist, this user info is not present in database"},
             "not found": {"status": "fail", "status_code": 404,
                           "error": "User Not found, User does not exists in data base"},
             "bad method": {"status": "fail", "status_code": 405,
                            "error": "Method not allowed, please use post method"},
             "unacceptable": {"status": "fail", "status_code": 406,
                              "error": "Request is not acceptable, accepted requests are login, register and update"},
             "empty field": {"status": "fail", "status_code": 406,
                             "error": "Request is not acceptable, user information can not be empty"},
             "unprocessable": {"status": "fail", "status_code": 422, "error": "JSON format is not correct"},
             "internal": {"status": "fail", "status_code": 500, "error": "Unexpected error in our database/server"}}

    if request.method != "POST":
        return jsonify(error["bad method"]), error["bad method"]["status_code"]

    if request.method != "POST":
        return jsonify(error["bad method"]), error["bad method"]["status_code"]

    request_json = request.get_json(silent=True)
    if isinstance(request_json, str):
        request_json = json.loads(request_json)
    elif type(request_json) != dict:
        return jsonify(error["bad request"]), error["bad request"]["status_code"]
    if not request_json:
        return jsonify(error["bad request"]), error["bad request"]["status_code"]

    necessary_info = ["userid", "video"]
    if not all(info in request_json for info in necessary_info):
        return jsonify(error["unprocessable"]), error["unprocessable"]["status_code"]

    necessary_info = ["title", "url"]
    if not all(info in request_json["video"] for info in necessary_info):
        return jsonify(error["unprocessable"]), error["unprocessable"]["status_code"]

    if not all(request_json["video"][info] for info in necessary_info):
        return jsonify(error["empty field"]), error["empty field"]["status_code"]

    # --------------Local testing connection string starts here---------------
    mysql = {"database": "video_sharing",
             "host": "35.232.179.75",
             "port": "127.0.0.1:3306",
             "connection": "cloudcomputinglab-291822:us-central1:cloud-computing",
             "username": "cloud-computing",
             "password": "cloud-computing",
             "drivername": "mysql+pymysql",
             "url": "mysql+pymysql://cloud-computing:cloud-computing@127.0.0.1:3306/video_sharing"
             }

    eng = create_engine(mysql["url"])

    # --------------Local testing connection string ends here------------------

    # ---------------------Cloud connection String starts here-----------

    # connection_name = "cloudcomputinglab-291822:us-central1:cloud-computing"
    # query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

    # eng = create_engine(
    #     engine.url.URL(
    #         drivername="mysql+pymysql",
    #         username="cloud-computing",
    #         password="cloud-computing",
    #         database="video_sharing",
    #         query=query_string,
    #     ),
    #     pool_size=5,
    #     max_overflow=2,
    #     pool_timeout=30,
    #     pool_recycle=1800
    # )
    # ------------------ Cloud connection string ends here------------------------

    db = scoped_session(sessionmaker(bind=eng))

    check_user_query = sqlalchemy.text("SELECT 1 FROM users WHERE id = :id")
    get_user_query = sqlalchemy.text("SELECT id, username, firstname, lastname, email, date_time"
                                     " FROM users")
    get_videos_query = sqlalchemy.text("SELECT * FROM videos")
    try:
        # user_in_db = db.execute(check_user_query, {"id": request_json["userid"]}).fetchall()
        user_in_db = db.execute(get_user_query).fetchall()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

    for user in user_in_db:
        print(user.id)

    if not user_in_db:
        return jsonify(error["forbidden"]), error["forbidden"]["status_code"]

    data = {"uploaded_by": request_json["userid"], "title": request_json["video"]["title"], "url": request_json["video"]["url"]}
    optional = ["tags", "description"]
    for info in optional:
        if info in request_json["video"]:
            data[info] = request_json["video"][info]
        else:
            data[info] = None

    if "privacy" in request_json["video"] and request_json["video"]["privacy"]:
        data["privacy"] = request_json["video"]["privacy"]
    else:
        data["privacy"] = 0

    insert_with_lastname_query = sqlalchemy.text("INSERT INTO videos (title, url, uploaded_by, "
                                                 "tags, description, privacy) "
                                                 "VALUES (:title, :url, :uploaded_by, "
                                                 ":tags, :description, :privacy)")
    print(insert_with_lastname_query)
    try:
        db.execute(insert_with_lastname_query, data)
        db.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

    try:
        videos_in_db = db.execute(get_videos_query).fetchall()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({"status": "fail", "status_code": 500, "error": error}), 500


    for video in videos_in_db:
        print(video)

    """Uploads a file to the bucket."""
    bucket_name = "video_360"

    # storage_client = storage.Client()
    storage_client = storage.Client.from_service_account_json(
        'C:/Users/Naveen S N/Downloads/CloudComputingLab-745a59e0bb6e.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(request_json["video"]["url"])
    print(blob)

    import urllib.request as req
    import cv2

    url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    req.urlretrieve(url, request_json["video"]["url"])
    cap = cv2.VideoCapture(request_json["video"]["url"])
    if cap.isOpened():
        ret, frame = cap.read()
        bucket = storage_client.bucket("videos_thumbnail")
        blob = bucket.blob(request_json["video"]["url"])

        cv2.imwrite(request_json["video"]["url"], frame)
        cv2.waitKey(0)
        blob.upload_from_filename(request_json["video"]["url"])
        os.remove(request_json["video"]["url"])

    return "success"
