from flask import jsonify


def allowed_file(file):
    if file.filename == "":
        jsonify({"error": "File not found"}), 400
    allowed_extensions = ['jpg', 'jpeg', 'png', 'jfif']
    filename,extension = file.filename.lower().split('.')
    if extension not in allowed_extensions:
        jsonify({"error":"Image format should be of format jpg/jpeg/png/jfif"}), 415
    return True