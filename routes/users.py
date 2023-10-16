from routes.postroutes import app
from flask import request, jsonify
from db import schemas
from db import user
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, current_user

bcrypt = Bcrypt(app)

@app.route("/register/user/", methods = ['POST'])
@jwt_required()
def create_user():
    user = current_user
    if not user:
        return jsonify({ "error": "User doesn't exist" }), 400
    if not user.issuperuser:
        return jsonify({ "error": "User not authorized to modify" }), 401
    try:
        user_data = schemas.user(**request.get_json())
        user_data = user.Users(email = user_data.email, country_code = user_data.country_code, phone_number = user_data.phone_number,
                               plan = user_data.plan, password = user_data.password, is_superuser = user_data.is_superuser)
        response = user_data.create_user()
        return response
    except Exception as e:
        return {"error":f"{str(e)}"}

@app.route("/login/", methods = ['GET'])
def login_func():

        login_credentials = schemas.login(**request.get_json())
        logs = user.Users()
        response = logs.login_func(login_credentials)
        return response
