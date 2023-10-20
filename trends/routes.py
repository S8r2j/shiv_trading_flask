from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, current_user
from db import schemas
from routes.utils import allowed_file
from db.model import trendingproduct
from trends.trend import Trending

trendrouter = Blueprint('trends', __name__)

@trendrouter.route("/trending/products/", methods = ['GET'])
def trending_products():
    product = Trending()
    response = product.get_trending_products()
    return response

@trendrouter.route("/untrend/products/", methods= ['DELETE'])
@jwt_required()
def del_trending_product():
    user = current_user
    if not user:
        return jsonify({ "error": "User doesn't exist" }), 400
    if not user.issuperuser:
        return jsonify({ "error": "User not authorized to modify" }), 401
    data = schemas.url(**request.get_json())
    product = Trending()
    response = product.delete_trending_product(photourl = data.photoaddress)
    return response