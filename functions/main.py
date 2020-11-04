import sqlalchemy
from flask import jsonify
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import json


def user_access(request):
    # mysql = {"database": "video_sharing",
    #          "host": "35.232.179.75",
    #          "port": "127.0.0.1:3306",
    #          "connection": "cloudcomputinglab-291822:us-central1:cloud-computing",
    #          "username": "cloud-computing",
    #          "password": "cloud-computing",
    #          "drivername": "mysql+pymysql",
    #          "url": "mysql+pymysql://cloud-computing:cloud-computing@127.0.0.1:3306/video_sharing"
    #          }
    #
    # eng = create_engine(mysql["url"])

    connection_name = "cloudcomputinglab-291822:us-central1:cloud-computing"
    query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

    eng = create_engine(
        engine.url.URL(
            drivername="mysql+pymysql",
            username="cloud-computing",
            password="cloud-computing",
            database="video_sharing",
            query=query_string,
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )

    db = scoped_session(sessionmaker(bind=eng))

    error = {"bad request": {"code": 400, "message": "No JSON, request should include JSON object"},
             "unauthorised": {"code": 401, "message": "Incorrect password, please enter correct password"},
             "forbidden": {"code": 403, "message": "Duplicate email, email id already exists"},
             "not found": {"code": 404, "message": "User Not found, User does not exists in data base"},
             "bad method": {"code": 405, "message": "Method not allowed, please use post method"},
             "unacceptable": {"code": 406, "message": "Request is not acceptable, "
                                                      "accepted requests are login, register and update"},
             "empty field": {"code": 406, "message": "Request is not acceptable, user information can not be empty"},
             "unprocessable": {"code": 422, "message": "JSON format is not correct"},
             "internal": {"code": 500, "message": "Unexpected error in our database/server"}}

    if request.method != "POST":
        return error["bad method"]["message"], error["bad method"]["code"]

    request_json = request.get_json(silent=True)
    if isinstance(request_json, str):
        request_json = json.loads(request_json)
    elif type(json.loads(request_json)) != dict:
        return error["bad request"]["message"], error["bad request"]["code"]
    if not request_json:
        return error["bad request"]["message"], error["bad request"]["code"]

    necessary_info = ["request", "data"]
    if not all(info in request_json for info in necessary_info):
        return error["unprocessable"]["message"], error["unprocessable"]["code"]

    check_user_query = sqlalchemy.text("SELECT 1 FROM users WHERE email = :email")
    get_user_query = sqlalchemy.text("SELECT id, username, firstname, lastname, email, date_time"
                                     " FROM users WHERE email = :email AND password = :password")

    if request_json["request"].lower() == "login":
        print("login")

        necessary_info = ["email", "password"]
        if not all(info in request_json["data"] for info in necessary_info):
            return error["unprocessable"]["message"], error["unprocessable"]["code"]

        if not all(request_json["data"][info] for info in necessary_info):
            return error["empty field"]["message"], error["empty field"]["code"]

        try:
            if db.execute(check_user_query, {"email": request_json["data"]["email"]}).fetchall():
                user = db.execute(get_user_query, request_json["data"]).fetchone()
                if user:
                    user = {"id": user[0], "username": user[1], "firstname": user[2],
                            "lastname": user[3], "email": user[4], "date_time": user[5]}
                    return jsonify(user)
                else:
                    return error["unauthorised"]["message"], error["unauthorised"]["code"]
            else:
                return error["not found"]["message"], error["not found"]["code"]

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error, 500

    elif request_json["request"].lower() == "register":

        print("register")
        necessary_info = ["username", "firstname", "email", "password"]
        if not all(info in request_json["data"] for info in necessary_info):
            return error["unprocessable"]["message"], error["unprocessable"]["code"]

        if not all(request_json["data"][info] for info in necessary_info):
            return error["empty field"]["message"], error["empty field"]["code"]

        try:
            user_in_db = db.execute(check_user_query, {"email": request_json["data"]["email"]}).fetchall()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error, 500

        if user_in_db:
            return error["forbidden"]["message"], error["forbidden"]["code"]

        if "lastname" in request_json["data"] and request_json["data"]["lastname"]:
            insert_with_lastname_query = sqlalchemy.text("INSERT INTO users (username, email, "
                                                         "firstname, lastname, password) "
                                                         "VALUES (:username, :email, :firstname, "
                                                         ":lastname, :password)")
            try:
                db.execute(insert_with_lastname_query,
                           request_json["data"])
                db.commit()
                # return "inserted with lastname"
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return error, 500

        else:
            insert_without_lastname_query = sqlalchemy.text("INSERT INTO users (username, email, firstname, password)"
                                                            "VALUES (:username, :email, :firstname, :password)")
            try:
                db.execute(insert_without_lastname_query,
                           request_json["data"])
                db.commit()

            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return error, 500

        try:
            user = db.execute(get_user_query, request_json["data"]).fetchone()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error, 500

        if user:
            user = {"id": user[0], "username": user[1], "firstname": user[2],
                    "lastname": user[3], "email": user[4], "date_time": user[5]}
            return jsonify(user), 201
        else:
            return error["unauthorised"]["message"], error["unauthorised"]["code"]

    else:
        return "you can only register or login"
        print("not register")

    #
    # tables = db.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
    # return jsonify([{key: value for key, value in row.items()} for row in tables if row is not None]), 200

    user = {"username": "Naveen",
            "email": "naveensn100@gmail.com",
            "firstname": "Naveen",
            "lastname": "Navn",
            "password": "asodasnasidndai"
            }
    #

    # db.execute("INSERT INTO users (id, username, email, firstname, lastname, password) ",
    #            "VALUES (, 'naveen', 'naveensn100@gmail.com', 'Naveen', 'S Na', 'asdasaxasdxasda')")
    # db.commit()

    db.execute("INSERT INTO users (username, email, firstname, lastname, password) "
               "VALUES (:username, :email, :firstname, :lastname, :password)",
               user)
    db.commit()

    stmt = sqlalchemy.text("SELECT * from users")
    users = db.execute(stmt).fetchall()
    if users is not None:
        return jsonify([{key: value for key, value in row.items()} for row in users if row is not None]), 200
    else:
        return jsonify([{}])

    # return jsonify({'greeting': 'Hello {}!'.format(escape(name + method))})
