def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

implicit()

def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'C:/Users/Naveen S N/Downloads/CloudComputingLab-745a59e0bb6e.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


explicit()

        uploaded_file = request.files['file']
        # c = checksumMD5(uploaded_file.stream)
        uploaded_file.seek(0)

        if uploaded_file.filename != '':
            url = 'http://127.0.0.1:8080/'
            print(request.files)
            print(uploaded_file)

            files = {"file": (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)}
            print(files)
            r = requests.post(url, files=files, json=dictToSend)
            # print(r.status_code)
            # print(request.files['file'])
            # uploaded_file.save(uploaded_file.filename)