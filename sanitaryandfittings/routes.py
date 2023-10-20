from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, current_user
from routes.utils import allowed_file
from sanitaryandfittings import fittings

firouter = Blueprint('sanitaryandfittings', __name__)

@firouter.route("/upload/cpfittings/photos/", methods=['POST'])
@jwt_required()
def upload_cpfittings_photos():
    user = current_user
    if not user:
        return jsonify({ "error": "User doesn't exist" }), 400
    if not user.issuperuser:
        return jsonify({ "error": "User not authorized to modify" }), 401
    product = request.args.get('product', type = str)
    fitting_name = request.args.get('fitting_name', type = str)
    trending = request.args.get('trending', type = str)
    description = request.form['description']
    up_photo = request.files['up_photo']
    if allowed_file(up_photo):
        fitting = fittings.Sanitary(product = product, fitting_name = fitting_name, file = up_photo, trend = trending, description = description)
        response = fitting.post_fittings()
        return response


@firouter.route("/cpfittings/photos/", methods = ['GET'])
def get_cpfitting_photos():
    fittingname = request.args.get('fittingname', default = None, type = str)
    fitting = fittings.Sanitary(fitting_name = fittingname)
    response = fitting.get_fittings()
    return response
