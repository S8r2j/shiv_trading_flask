from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, current_user
from graniteandmarbles import granitemarbel
from routes.postroutes import allowed_file

grrouter = Blueprint('graniteandmarbles', __name__)

@grrouter.route("/upload/granite&marble/photos/", methods=['POST'])
@jwt_required()
def upload_granite_photos():
    user = current_user
    if not user:
        return jsonify({ "error": "User doesn't exist" }), 400
    if not user.issuperuser:
        return jsonify({ "error": "User not authorized to modify" }), 401
    product = request.args.get('product', type = str)
    granite = request.args.get('granite', type = str)
    thik = request.args.get('thick', type = str)
    trending = request.args.get('trending', type = str)
    file = request.files["up_photo"]

    if allowed_file(file = file):
        gr = granitemarbel.Marbles(product = product, granite = granite, thik = thik, file = file, trend = trending)
        response = gr.post_granites()
        return response


@grrouter.route("/granite/photos/", methods = ['GET'])
def get_granite_photos():
    granite = request.args.get('granite', default = None, type = str)
    thik = request.args.get('thick', default = None, type = str)
    gr = granitemarbel.Marbles(granite = granite, thik = thik)
    response = gr.get_granites()
    return response
