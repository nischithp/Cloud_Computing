import sqlalchemy
from flask import escape, jsonify, request, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def user_access(request):
    connection_name = "cloudcomputinglab-291822:us-central1:cloud-computing"

    mysql = {"database": "video_sharing",
             "host": "35.232.179.75",
             "port": "127.0.0.1:3306",
             "connection": "cloudcomputinglab-291822:us-central1:cloud-computing",
             "user_name": "cloud-computing",
             "password": "cloud-computing",
             "driver": "mysql+pymysql",
             "url": "mysql+pymysql://cloud-computing:cloud-computing@127.0.0.1:3306/video_sharing"
             }
    query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

    engine = create_engine(mysql["url"])
    db = scoped_session(sessionmaker(bind=engine))

    error = {"bad request": {"code": 400, "message": "No JSON, request should include JSON object"},
             "unauthorised": {"code": 401, "message": "Incorrect password, please enter correct password"},
             "forbidden": {"code": 403, "message": "Duplicate email, email id already exists"},
             "not found": {"code": 404, "message": "User Not found, User does not exists in data base"},
             "bad method": {"code": 405, "message": "Method not allowed, please use post method"},
             "unacceptable": {"code": 406, "message": "Request is not acceptable, "
                                                      "accepted requests are login, register and update"},
             "unprocessable": {"code": 422, "message": "JSON format is not correct"},
             "internal": {"code": 500, "message": "Unexpected error in our database/server"}}

    # print("request.method: ", request.method)
    # print("request.method: ", request.method)
    # print("request.headers: ", request.headers)

    if request.method != "POST":
        return error["bad method"]["message"], error["bad method"]["code"]

    request_json = request.get_json(silent=True)

    if not request_json:
        return error["bad request"]["message"], error["bad request"]["code"]
    if "request" not in request_json or "data" not in request_json:
        return error["unprocessable"]["message"], error["unprocessable"]["code"]

    check_user_query = sqlalchemy.text("SELECT 1 FROM users WHERE email = :email")
    if request_json["request"].lower() == "login":

        if "email" not in request_json["data"] or "password" not in request_json["data"]:
            return error["unprocessable"]["message"], error["unprocessable"]["code"]

        if db.execute(check_user_query, {"email": request_json["data"]["email"]}).fetchall():
            get_user_query = sqlalchemy.text("SELECT id, username, firstname, lastname, date_time"
                                             " FROM users WHERE email = :email AND password = :password")
            user = db.execute(get_user_query, request_json["data"]).fetchone()

            if user:
                user = {"id": user[0], "username": user[1], "firstname": user[2],
                        "lastname": user[3], "date_time": user[4]}
                return jsonify(user)
            else:
                return error["unauthorised"]["message"], error["unauthorised"]["code"]
        else:
            return error["not found"]["message"], error["not found"]["code"]

    elif request_json["request"].lower() == "register":

        necessary_info = ["username", "firstname", "email", "password"]
        if all(info in request_json["data"] for info in necessary_info):

            if db.execute(check_user_query, {"email": request_json["data"]["email"]}).fetchall():
                return error["forbidden"]["message"], error["forbidden"]["code"]

            if "lastname" in request_json["data"] and request_json["data"]["lastname"]:
                insert_with_lastname_query = sqlalchemy.text("INSERT INTO users (username, email, "
                                                             "firstname, lastname, password) "
                                                             "VALUES (:username, :email, :firstname, "
                                                             ":lastname, :password)")
                try:
                    db.execute(insert_with_lastname_query,
                               request_json["data"])
                    return "inserted with lastname"
                except:
                    return "except with"


            else:
                insert_without_lastname_query = sqlalchemy.text("INSERT INTO users (username, email, "
                                                                "firstname, password) "
                                                                "VALUES (:username, :email, :firstname, :password)")

                try:
                    db.execute(insert_without_lastname_query,
                           request_json["data"])
                except:
                    return "except without"

                return "inserted without lastname"

            db.commit()

        else:
            return error["unprocessable"]["message"], error["unprocessable"]["code"]

    #
    # tables = db.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
    # return jsonify([{key: value for key, value in row.items()} for row in tables if row is not None]), 200

    user = {"username": "Naveen",
            "email": "naveensn100@gmail.com",
            "firstname": "Naveen",
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

    users = db.execute(stmt).fetchall()
    if users is not None:
        return jsonify([{key: value for key, value in row.items()} for row in users if row is not None]), 200
    else:
        return jsonify([{}])

    # return jsonify({'greeting': 'Hello {}!'.format(escape(name + method))})
