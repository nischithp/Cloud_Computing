import sqlalchemy
from flask import jsonify
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import json


def user_access(request):
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
    #------------------ Cloud connection string ends here------------------------

    db = scoped_session(sessionmaker(bind=eng))

    error = {"bad request": {"status": "fail", "status_code": 400,
                             "error": "No JSON, request should include JSON object"},
             "unauthorised": {"status": "fail", "status_code": 401,
                              "error": "Incorrect password, please enter correct password"},
             "forbidden": {"status": "fail", "status_code": 403,
                           "error": "Duplicate email, email id already exists"},
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

    request_json = request.get_json(silent=True)
    if isinstance(request_json, str):
        request_json = json.loads(request_json)
    elif type(request_json) != dict:
        return jsonify(error["bad request"]), error["bad request"]["status_code"]
    if not request_json:
        return jsonify(error["bad request"]), error["bad request"]["status_code"]

    necessary_info = ["request", "data"]
    if not all(info in request_json for info in necessary_info):
        return jsonify(error["unprocessable"]), error["unprocessable"]["status_code"]

    check_user_query = sqlalchemy.text("SELECT 1 FROM users WHERE email = :email")
    get_user_query = sqlalchemy.text("SELECT id, username, firstname, lastname, email, date_time"
                                     " FROM users WHERE email = :email AND password = :password")
    update_user_query = sqlalchemy.text("SELECT * FROM users")

    if request_json["request"].lower() == "login":

        necessary_info = ["email", "password"]
        if not all(info in request_json["data"] for info in necessary_info):
            return jsonify(error["unprocessable"]), error["unprocessable"]["status_code"]

        if not all(request_json["data"][info] for info in necessary_info):
            return jsonify(error["empty field"]), error["empty field"]["status_code"]

        try:
            if db.execute(check_user_query, {"email": request_json["data"]["email"]}).fetchall():
                user = db.execute(get_user_query, request_json["data"]).fetchone()
                if user:
                    user = {"id": user[0], "username": user[1], "firstname": user[2],
                            "lastname": user[3], "email": user[4], "date_time": user[5]}
                    return jsonify({"status": "success", "status_code": 200, "data": user})
                else:
                    return jsonify(error["unauthorised"]), error["unauthorised"]["status_code"]
            else:
                return jsonify(error["not found"]), error["not found"]["status_code"]

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

    elif request_json["request"].lower() == "register":

        necessary_info = ["username", "firstname", "email", "password"]
        if not all(info in request_json["data"] for info in necessary_info):
            return jsonify(error["unprocessable"]), error["unprocessable"]["status_code"]

        if not all(request_json["data"][info] for info in necessary_info):
            return jsonify(error["empty field"]), error["empty field"]["status_code"]

        try:
            user_in_db = db.execute(check_user_query, {"email": request_json["data"]["email"]}).fetchall()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

        if user_in_db:
            return jsonify(error["forbidden"]), error["forbidden"]["status_code"]

        if "lastname" in request_json["data"] and request_json["data"]["lastname"]:
            insert_with_lastname_query = sqlalchemy.text("INSERT INTO users (username, email, "
                                                         "firstname, lastname, password) "
                                                         "VALUES (:username, :email, :firstname, "
                                                         ":lastname, :password)")
            try:
                db.execute(insert_with_lastname_query,
                           request_json["data"])
                db.commit()

            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

        else:
            insert_without_lastname_query = sqlalchemy.text("INSERT INTO users (username, email, firstname, password)"
                                                            "VALUES (:username, :email, :firstname, :password)")
            try:
                db.execute(insert_without_lastname_query,
                           request_json["data"])
                db.commit()

            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

        try:
            user = db.execute(get_user_query, request_json["data"]).fetchone()

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

        if user:
            user = {"id": user[0], "username": user[1], "firstname": user[2],
                    "lastname": user[3], "email": user[4], "date_time": user[5]}
            return jsonify({"status": "success", "status_code": 201, "data": user}), 201
        else:
            return jsonify(error["unauthorised"]), error["unauthorised"]["status_code"]
    
    # To handle the update operations for the API
    elif request_json["request"].lower() == "update":
        userID = request_json["data"]["id"]
        oldPassword = request_json["data"]["oldPassword"]
        newPassword = request_json["data"]["newPassword"]
        password_compare_query = sqlalchemy.text("select id from users where id="+userID+" and password='"+oldPassword+"'")
        passwordUpdateQuery = sqlalchemy.text("UPDATE users SET password='"+newPassword+"' WHERE id="+userID)

        # Check to see if the old and new passwords are same. If not, do not even proceed further.
        try:
            comparisonResult = db.execute(password_compare_query).fetchone()
            print (comparisonResult)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"status": "fail", "status_code": 500, "error": error}), 500

        # Check if comaparisonResult is set from the earlier query. If it is, then execute the update query and commit the transaction, else send a 401 response.
        if comparisonResult:
            try:
                updateResult = db.execute(passwordUpdateQuery)
                db.commit()
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return jsonify({"status": "fail", "status_code": 500, "error": error}), 500
            
            print(updateResult)
            # Check to see if the cursor's updated rows is 1, to denote succesful update, else send error
            if updateResult:
                return jsonify({"status": "success", "status_code": 200, "data":"password updated"}), 200
            else:
                return jsonify({"status": "fail", "status_code": 422, "error":"Missing or Invalid Data"}), 422

        else:
            return jsonify({"status": "unauthorized", "status_code": 401, "error": "old and new passwords do not match"}), 401
    else:
        return "you can only register or login"

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
