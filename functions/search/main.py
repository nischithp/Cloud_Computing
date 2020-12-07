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
    {   search: "play now"
    }
Enters user video details in SQL database and creates video thumbnail.
'''


def search(request):
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

    if "search" in request_json and request_json["search"]:
        search_string = request_json["search"]
        search_words = search_string.split()
        first_word = search_words.pop(0)
        search_words_title = "title LIKE '%" + first_word + "%'"
        search_words_tags = "tags LIKE '%" + first_word + "%'"
        Search_words_description = "description LIKE '%" + first_word + "%'"
        for word in search_words:
            search_words_title += " OR title LIKE '%" + word + "%'"
            search_words_tags += " OR tags LIKE '%" + word + "%'"
            Search_words_description += " OR description LIKE '%" + word + "%'"
        get_videos_query = sqlalchemy.text("SELECT url FROM videos where (" + search_words_title +
                                           " OR " + search_words_tags +
                                           " OR " + Search_words_description +
                                           ") and privacy = 0")
    else:
        get_videos_query = sqlalchemy.text("SELECT url FROM videos where privacy = 0")

    try:
        print(get_videos_query)
        videos_in_db = db.execute(get_videos_query).fetchall()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

    data = {"videos": []}
    for video in videos_in_db:
        print(video.url)
        data["videos"].append(video.url)
    return jsonify(data)

