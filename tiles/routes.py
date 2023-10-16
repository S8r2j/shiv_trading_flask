from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, current_user
from routes.postroutes import allowed_file
from tiles import tiles

tirouter = Blueprint('tiles', __name__)

@tirouter.route('/upload/tiles/photos/', methods=['POST'])
@jwt_required()
def upload_photo():
    user = current_user
    if not user:
        return jsonify({ "error": "User doesn't exist" }), 400
    if not user.issuperuser:
        return jsonify({ "error": "User not authorized to modify" }), 401
    product = request.args.get('product', type = str)
    size = request.args.get('size', type = str)
    room = request.args.get('room', type = str)
    trending = request.args.get('trending', type=str)
    file = request.files['up_photo']
    if allowed_file(file):
        tile = tiles.Tiles(product = product, room = room, size = size, file = file, trend = trending)
        response = tile.post_tiles()
        return response


@tirouter.route("/tiles/photos/", methods = ['GET'])
def get_tiles_photos():
    product = request.args.get('product', default = None, type = str)
    size = request.args.get('size', default = None, type = str)
    room = request.args.get('room', default = None, type = str)
    tile = tiles.Tiles(product = product, size = size, room = room)
    response = tile.get_tiles()
    return response