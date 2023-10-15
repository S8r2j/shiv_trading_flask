import tempfile
from flask import abort
from routes import imagekit

def upload_photo(file,folder)->str:
    class Object:
        def __init__(self):
            self.folder = f'/{folder}/'
    obj = Object()
    filename, extension = file.filename.split(".")
    temp_file = tempfile.NamedTemporaryFile(delete = False)
    file.save(temp_file)
    # Upload the image to ImageKit
    try:
        upload_response = imagekit.upload_file(
                file = open(temp_file.name, 'rb'),
                file_name = filename,
                options = obj
            )
    except Exception as e:
        abort(500, description = {"error":str(e)})
    temp_file.close()
    url_str = str(upload_response.url)
    return url_str