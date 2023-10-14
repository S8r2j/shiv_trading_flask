from flask import request, abort, Response, json, jsonify
import io
from db.model import db, products, sizes, rooms, tilesphotos, productroomsize, cpfittings, cpphotos, productfitting,granites,granitethick,granitephoto, thick
from routes import imagekit
from routes import upphoto
from routes.getroutes import app
from core.config import settings
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import imagekitio
import tempfile



def allowed_file(file):
    max_size = 10  # 10MB
    if file.filename == "":
        abort(404, description = "File not found")
    allowed_extensions = ['jpg', 'jpeg', 'png', 'jfif']
    filename,extension = file.filename.lower().split('.')
    if extension not in allowed_extensions:
        abort(415, description = "Image can be of jpg/jpeg/png/jfif formats only")
    return True

@app.route('/upload/tiles/photos/', methods=['POST'])
def upload_photo():
    product = request.args.get('product', type = str)
    size = request.args.get('size', type = str)
    room = request.args.get('room', type = str)
    ## Get the unique number for each of the products
    query = products.query.filter(products.productname == product).first()
    if not query:
        abort(404)

    query = sizes.query.filter(sizes.sizes == size).first()
    if not query:
        abort(404)

    query = rooms.query.filter(rooms.roomname == room).first()
    if not query:
        abort(404)

    tile_type = productroomsize.query.join(products).join(sizes).join(rooms).filter(
        products.productname == product,
        rooms.roomname == room,
        sizes.sizes == size
    ).first()
    ## Got the unique number

    file = request.files['photo']
    if allowed_file(file):
            # Get the URL of the uploaded image
        image_url = upphoto.upload_photo(file,"tiles")
        photo_address = image_url
        with app.app_context():
            upload_photo = tilesphotos(photoaddress = photo_address, prsid = tile_type.prsid)
            db.session.add(upload_photo)
            db.session.commit()

        return { "message": "Photo uploaded successfully" }