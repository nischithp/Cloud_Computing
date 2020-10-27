import sqlalchemy
from flask import escape, jsonify, request, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy


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

    class user:
        def __index__(self, user_id, username, email, firstname, lastname, password, register_time):
            self.user_id = user_id
            self.username = username
            self.email = email
            self.firstname = firstname
            self.lastname = lastname
            self.password = password
            self.register_time = register_time


    # print("request.method: ", request.method)
    # print("request.method: ", request.method)
    # print("request.headers: ", request.headers)
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'

    tables = db.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
    return jsonify([{key: value for key, value in row.items()} for row in tables if row is not None]), 200

    stmt = sqlalchemy.text('select * from user')

    user = {"username": "Naveen",
            "email": "naveensn100@gmial.com",
            "firstname": "Naveen",
            "lastname": "S N",
            "password": "asodasnasidndai"
           }

    db.execute("DROP TABLE user")

    db.execute("CREATE TABLE users ("
               "id SERIAL PRIMARY KEY,"
               "username VARCHAR NOT NULL,"
               "email VARCHAR NOT NULL,"
               "firstname VARCHAR NOT NULL,"
               "lastname VARCHAR,"
               "password VARCHAR NOT NULL,"
               "date_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP)")

    db.execute("INSERT INTO users (username, email, firstname, lastname, password) "
               "VALUES (:username, :email, :firstname, :lastname, password)",
              user)
    db.commit()



    users = db.execute(stmt).fetchall()
    if users is not None:
        return jsonify([{key: value for key, value in row.items()} for row in users if row is not None]), 200
    else:
        return jsonify([{}])



    #return jsonify({'greeting': 'Hello {}!'.format(escape(name + method))})
