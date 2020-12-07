import sqlalchemy
from flask import jsonify
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import json

'''
Called by HTTP request,
input JSON: Contains userid and information about video uploaded
    {   search: "play now"
    }
Enters user video details in SQL database and creates video thumbnail.
'''


def search():
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
    #
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
    delete_videos = sqlalchemy.text("DELETE FROM videos")
    try:
        db.execute(delete_videos)
        db.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({"status": "fail", "status_code": 500, "error": error}), 500


    get_videos_query = sqlalchemy.text("SELECT url FROM videos")
    try:
        videos_in_db = db.execute(get_videos_query).fetchall()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

    for video in videos_in_db:
        print(video)

search()