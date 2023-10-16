from flask import jsonify
from core.config import settings
from db import model

from flask_jwt_extended import create_access_token, current_user, JWTManager
app = model.app
app.config['JWT_SECRET_KEY']= f'{settings.SECRET_KEY}'

jwt = JWTManager(app)

class Token:

    def generate_token(self, identity):
        token = create_access_token(identity = identity)
        return token

@jwt.user_identity_loader
def user_identity_lookup(id):
    return id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    with app.app_context():
        query = model.user.query.join(model.login).filter(model.login.sn == identity).first()
        if not query:
            return None
        else:
            return query