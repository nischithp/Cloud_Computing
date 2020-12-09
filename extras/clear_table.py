import sqlalchemy
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

'''
Called by HTTP request,
input JSON: Contains userid and information about video uploaded
    {   search: "play now"
    }
Enters user video details in SQL database and creates video thumbnail.
'''


def clear():
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

    engine = create_engine(mysql["url"])

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

    db = scoped_session(sessionmaker(bind=engine))

    # delete_videos = sqlalchemy.text("DELETE FROM videos")
    # try:
    #     db.execute(delete_videos)
    #     db.commit()
    #
    # except SQLAlchemyError as e:
    #     error = str(e.__dict__['orig'])
    #     return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

    get_videos_query = sqlalchemy.text("SELECT * FROM videos")
    try:
        videos_in_db = db.execute(get_videos_query).fetchall()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

    for video in videos_in_db:
        print(video)

clear()