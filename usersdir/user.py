from db.model import app
from datetime import datetime, timedelta
from flask import abort, jsonify
from db import model
from db import schemas, tokencrud
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, current_user



bcrypt = Bcrypt(app)

class Users:
    def __init__(self,email = None, country_code = None, phone_number = None, plan = None, password = None, is_superuser = None):
        self.email = email
        self.country_code = country_code
        self.phone_number = phone_number
        self.plan = plan
        self.password = password
        self.is_superuser = is_superuser

    @jwt_required()
    def create_user(self):
        user = current_user
        if not user:
            return jsonify({"error":"User doesn't exist"}), 400
        if not user.issuperuser:
            return jsonify({"error":"User not authorized to modify"}),401
        with app.app_context():
            usr_phone = model.user.query.filter(model.user.phonenumber == self.phone_number).first()
            usr_email = model.user.query.filter(model.user.email == self.email).first()
            if usr_email or usr_phone:
                return jsonify({"error":"User with the email or phonenumber already exists"}),409
            user_create = model.user(
                email = self.email, countrycode = self.country_code, phonenumber = self.phone_number,
                issuperuser = self.is_superuser, plan = self.plan
                )
            model.db.session.add(user_create)
            model.db.session.commit()
            model.db.session.refresh(user_create)
            users = model.user.query.filter(model.user.phonenumber == self.phone_number).first()
            password = bcrypt.generate_password_hash(self.password).decode('utf-8')
            login_create = model.login(id = users.id, password = password)
            model.db.session.add(login_create)
            model.db.session.commit()
            model.db.session.refresh(login_create)
            login_query = model.login.query.filter(model.login.id == users.id).first()
            if not login_query.sn:
                model.db.session.delete(users)
                abort(500, description = "Account not created! Please try again later")

        return "User created! Please proceed to login"

    def login_func(self, login_credentials:schemas.login):
        user_data = model.login.query.join(model.user).filter(
            model.user.phonenumber == login_credentials.phonenumber
            ).first()
        if not user_data:
            abort(404, description = "Please login to proceed")
        issuccess = bcrypt.check_password_hash(user_data.password, login_credentials.password)
        if not issuccess:
            abort(401, description = "Invalid credentials")
        else:
            tokn = tokencrud.Token()
            return {
                "message":"Login Successful",
                "token":f"{tokn.generate_token(user_data.sn)}"
            }

    @jwt_required()
    def remove_users(self, phonenumber):
        users = current_user
        if not users:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not users.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        user = model.user.query.filter(model.user.phonenumber == phonenumber).first()
        if not user:
            return jsonify({ "error": "User not found" }), 400
        credentials = model.login.query.join(model.user).filter(model.user.phonenumber == user.phonenumber).first()
        if not credentials:
            model.db.session.delete(user)
            model.db.session.commit()
            return jsonify({ "error": "Login credentials not found for the user" }), 400
        try:
            model.db.session.delete(credentials)
            model.db.session.commit()
            model.db.session.delete(user)
            model.db.session.commit()
            return "Successfully removed the user"
        except Exception as e:
            return jsonify(f"error: {str(e)}"), 500


    @jwt_required()
    def change_plans(self, phonenumber, plan):
        users = current_user
        if not users:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not users.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        plan_list = ['BASIC', 'STANDARD', 'PREMIUM']
        if plan.upper() not in plan_list:
            return jsonify("error: No such plans exist"), 400
        user = model.user.query.filter(model.user.phonenumber == phonenumber).first()
        if not user:
            return jsonify("error: No user found"), 400
        user.plan = plan
        user.expiresat = datetime.utcnow() + timedelta(days = 28)
        model.db.session.commit()
        return "Plan updated successfully"