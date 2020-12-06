from flask import jsonify
from google.cloud import storage


def upload(request):
    print("got request")
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

    print(request.method)
    if request.method != "POST":
        return jsonify(error["bad method"]), error["bad method"]["status_code"]

    # print(request.files)
    f = request.files['file']
    print(f)
    """Uploads a file to the bucket."""
    bucket_name = "video_360"
    # source_file_name = "local/path/to/file"
    print(f.filename)

    destination_blob_name = f.filename

    # storage_client = storage.Client()
    storage_client = storage.Client.from_service_account_json(
        'C:\Users\nisch\Downloads\cloudcomputinglab-291822-bf0774247e88.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(f)

    print(
        "File {} uploaded to {}.".format(
            f.filename, destination_blob_name
        )
    )
    return "success"
