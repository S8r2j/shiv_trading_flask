from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from finishes.finish import Finishing
from routes.utils import allowed_file

finishrouter = Blueprint('finishes', __name__)

@finishrouter.route('/finish/photos/', methods = ['GET'])
@jwt_required()
def finish_photos():
    user = current_user
    if not user:
        return jsonify({ "error": "User doesn't exist" }), 400
    if not user.issuperuser:
        return jsonify({ "error": "User not authorized to modify" }), 401
    plan = request.args.get('plan', type = str)
    finish = Finishing(plan = plan)
    response = finish.get_finish_photos()
    return response

@finishrouter.route('/upload/finish/photos/', methods = ['POST'])
@jwt_required()
def upload_finish_photos():
    user = current_user
    if not user:
        return jsonify({ "error": "User doesn't exist" }), 400
    if not user.issuperuser:
        return jsonify({ "error": "User not authorized to modify" }), 401
    plan = request.args.get('plan', type = str)
    description = request.form['description']
    file = request.files['up_photo']
    if allowed_file(file):
        finish = Finishing(plan = plan, description = description)
        response = finish.post_finish_photos(file = file)
        print(response)
        return response