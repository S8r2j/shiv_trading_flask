from db import model
from core.config import settings
from usersdir.user import bcrypt

def create_owner():
    with model.app.app_context():
        exist_owner = model.user.query.first()
        if not exist_owner:
                create_owner = model.user(email = settings.OWNER_EMAIL, phonenumber = settings.OWNER_PHONE, plan = settings.OWNER_PLAN,
                                          countrycode = settings.OWNER_COUNTRY, issuperuser = True)
                model.db.session.add(create_owner)
                model.db.session.commit()
                model.db.session.refresh(create_owner)
                owner = model.user.query.filter(model.user.phonenumber == settings.OWNER_PHONE).first()
                owner_login = model.login(id = owner.id, password = bcrypt.generate_password_hash(settings.OWNER_PASSWORD))
                model.db.session.add(owner_login)
                model.db.session.commit()
                model.db.session.refresh(owner_login)