from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.cloud import storage
from moviepy.editor import VideoFileClip
import os
from PIL import Image
# from helper import create_thumbmail, upload_file

app = Flask(__name__)

url = 'http://127.0.0.1:8080/'
dictToSend = {"data": {"email": "aaa@gmial.com",
                       "password": "71237**123712383",
                       "username": "123",
                       "firstname": "123",
                       "lastname": "123"},
              "request": "login"}

ALLOWED_SIZE = 100*1024*1024*1024
ALLOWED_EXTENSIONS = set(['mpg', 'mpeg', 'mp4'])



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        print("size =", request.content_length)
        if f.filename != '':
            print(f)
            """Uploads a file to the bucket."""
            bucket_name = "video_360"
            # source_file_name = "local/path/to/file"
            print(f.filename)

            destination_blob_name = f.filename

            # storage_client = storage.Client()
            storage_client = storage.Client.from_service_account_json(
                'C:/Users/Naveen S N/Downloads/CloudComputingLab-745a59e0bb6e.json')
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            a = blob.upload_from_file(f)
            print(a)

            print(
                "File {} uploaded to {}.".format(
                    f.filename, destination_blob_name
                )
            )

            blob = bucket.get_blob(destination_blob_name)
            print(blob)

            clip = VideoFileClip()
            clip.save_frame("thumbnail.jpg", t=1.00)

            metadata = {'color': 'Red', 'name': 'Test'}
            blob.metadata = metadata

            print("The metadata for the blob {} is {}".format(blob.name, blob.metadata))

            print("Blob: {}".format(blob.name))
            print("Bucket: {}".format(blob.bucket.name))
            print("Storage class: {}".format(blob.storage_class))
            print("ID: {}".format(blob.id))
            print("Size: {} bytes".format(blob.size))
            print("Updated: {}".format(blob.updated))
            print("Generation: {}".format(blob.generation))
            print("Metageneration: {}".format(blob.metageneration))
            print("Etag: {}".format(blob.etag))
            print("Owner: {}".format(blob.owner))
            print("Component count: {}".format(blob.component_count))
            print("Crc32c: {}".format(blob.crc32c))
            print("md5_hash: {}".format(blob.md5_hash))
            print("Cache-control: {}".format(blob.cache_control))
            print("Content-type: {}".format(blob.content_type))
            print("Content-disposition: {}".format(blob.content_disposition))
            print("Content-encoding: {}".format(blob.content_encoding))
            print("Content-language: {}".format(blob.content_language))
            print("Metadata: {}".format(blob.metadata))
            print("Custom Time: {}".format(blob.custom_time))
            print("Temporary hold: ", "enabled" if blob.temporary_hold else "disabled")
            print(
                "Event based hold: ",
                "enabled" if blob.event_based_hold else "disabled",
            )
            if blob.retention_expiration_time:
                print(
                    "retentionExpirationTime: {}".format(
                        blob.retention_expiration_time
                    )
                )
            return render_template('index.html', message="Done")
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/view/', methods=['GET', 'POST'])
def view():
    return render_template('view.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        size = request.content_length

        if not file:
            print("No File to Upload.")
            status="No File to Upload."

        elif size > ALLOWED_SIZE:
            print ("File size more then 10Mb.")
            status="File size more then 10Mb."

        elif '.' in file.filename and file.filename.split('.', 1)[1] not in ALLOWED_EXTENSIONS:
            print("This file extesion not allowed.")
            status="This file extesion not allowed."

        else:
            try:
                thumbnail_bucket_name = "videos_thumbnail"
                bucket_name = "videos_360"
                # source_file_name = "local/path/to/file"
                print(file.filename)

                destination_blob_name = file.filename

                # Creating thumbnail file:

                print(file.stream)


                # vs = file.stream
                # image_name = destination_blob_name.split('.')[0] + '.jpeg'
                # frame = vs.get_frame_at_sec(10)
                # img = frame.image()
                # img = img.resize((300, 300))
                # img.save('{0}.jpeg'.format(image_name))

                # linking storage
                storage_client = storage.Client.from_service_account_json(
                    'C:/Users/Naveen S N/Downloads/CloudComputingLab-745a59e0bb6e.json')

                # Uploading thumbnail
                # Setting destination name
                thumbnail_bucket = storage_client.bucket(thumbnail_bucket_name)
                # thumbnail_blob = thumbnail_bucket.blob(image_name)

                # thumbnail_blob.upload_from_file(img)

                # uploading video file
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)

                blob.upload_from_file(file)

                print(
                    "File {} uploaded to {}.".format(
                        file.filename, destination_blob_name
                    )
                )

                filename = file.filename,
                status = "Uploaded"

            except Exception as e:
                print(e)
                status="Failed to upload. Some error occured."

        return render_template('index.html', message=status)
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=True, port=port)
    # app.run(host='0.0.0.0', port=port)
