import tempfile
from flask import abort, jsonify
from routes import imagekit

def upload_photo(file,folder)->dict:
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
    return {
        "url": url_str,
        "file_id": upload_response.file_id
    }

def delete_photos(fileid):
    try:
        delete = imagekit.delete_file(file_id = fileid)
        return "Deleted Successfully"
    except Exception as e:
        return jsonify(f"error: {str(e)}"), 500