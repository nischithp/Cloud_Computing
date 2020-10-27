import sqlalchemy
from flask import escape, jsonify, request, make_response
import sqlalchemy as sql


def user_access(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    # connection_name = "cloudcomputinglab-291822:us-central1:cloud-computing"
    connection_name = "cloudcomputinglab-291822:us-central1:cloud-computing"

    table_name = ""
    table_field = ""
    table_field_value = ""
    db_name = "video_sharing"
    db_user = "root"
    db_password = "admin"

    driver_name = 'mysql+pymysql'
    query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

    db = sql.create_engine(sql.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )

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

    stmt = sqlalchemy.text('select * from user')
    try:
        with db.connect() as conn:
            conn.execute(stmt)
    except Exception as e:
        return 'Error: {}'.format(str(e))
    return 'ok'

    return jsonify({'greeting': 'Hello {}!'.format(escape(name + method))})
