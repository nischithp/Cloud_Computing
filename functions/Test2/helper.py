from app import app
from ffmpeg import VideoStream
from werkzeug import secure_filename
import os

def create_thumbmail(file):
    vs = VideoStream(file)
    image_name = imagename.split('.')[0]
    frame = vs.get_frame_at_sec(10)
    img = frame.image()
    img = img.resize((300,300))
    img.save('{0}.jpeg'.format(image_name))


def upload_file(file):
    filename = secure_filename(file.filename)
    full_pathname = os.path.join(UPLOAD_FOLDER, filename)
    full_pathname_image = os.path.join(UPLOAD_FOLDER_IMAGES, filename)
    file.save(full_pathname)
    create_thumbmail(full_pathname, full_pathname_image)