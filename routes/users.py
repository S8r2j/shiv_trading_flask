from routes.postroutes import app, db
from flask import request, abort
from db import schemas
from db.model import user, login
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/register/user/", methods = ['POST'])
def create_user():
    try:
        user_data = schemas.user(**request.get_json())
        with app.app_context():
            user_create = user(email = user_data.email, countrycode = user_data.country_code, phonenumber = user_data.phone_number, issuperuser = user_data.is_superuser, plan = user_data.plan)
            db.session.add(user_create)
            db.session.commit()
            db.session.refresh(user_create)
            users = user.query.filter(user.phonenumber == user_data.phone_number).first()
            password = bcrypt.generate_password_hash(user_data.password).decode('utf-8')
            login_create = login(id = users.id, password = password)
            db.session.add(login_create)
            db.session.commit()
            db.session.refresh(login_create)
    except Exception as e:
        return {"error":f"{(str(e))}"}
    return "User created! Please proceed to login"

@app.route("/login/", methods = ['GET'])
def login_func():
    try:
        login_credentials = schemas.login(**request.get_json())
        print(login_credentials.password)
        user_data = login.query.join(user).filter(user.phonenumber == login_credentials.phonenumber).first()
        issuccess = bcrypt.check_password_hash(user_data.password,login_credentials.password)
        print(issuccess)
        if not issuccess:
            abort(401, description = "Invalid credentials")
        else:
            return "Login Successful"
    except Exception as e:
        return {"error": f"{str(e)}"}