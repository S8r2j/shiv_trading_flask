from routes.postroutes import app
from flask import abort
from db import model
from db import schemas
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class Users:
    def __init__(self,email = None, country_code = None, phone_number = None, plan = None, password = None, is_superuser = None):
        self.email = email
        self.country_code = country_code
        self.phone_number = phone_number
        self.plan = plan
        self.password = password
        self.is_superuser = is_superuser
    def create_user(self):
            try:
                with app.app_context():
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
            except Exception as e:
               return { "error": f"{(str(e))}" }

            return "User created! Please proceed to login"

    def login_func(self, login_credentials:schemas.login):
        user_data = model.login.query.join(model.user).filter(
            model.user.phonenumber == login_credentials.phonenumber
            ).first()
        issuccess = bcrypt.check_password_hash(user_data.password, login_credentials.password)
        if not issuccess:
            abort(401, description = "Invalid credentials")
        else:
            return "Login Successful"