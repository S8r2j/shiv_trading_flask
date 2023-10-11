from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from core.config import settings

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?charset=utf8mb4"
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    country_code=db.Column(db.String(5),nullable=False)
    phone_number = db.Column(db.String(11), unique=True, nullable=False)
    plan=db.Column(db.String(20),nullable=False)
    is_superuser=db.Column(db.Boolean, default = False)
    login = db.relationship('login', backref = 'user', uselist= False)


class login(db.Model):
    sn=db.Column(db.Integer,autoincrement=True,primary_key=True)
    id=db.Column(db.Integer,db.ForeignKey("user"),nullable=False)
    pasword=db.Column(db.String(50),nullable=False)


class products(db.Model):
    p_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    product_name=db.Column(db.String(100),nullable=False)


class sizes(db.Model):
    s_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    sizes=db.Column(db.Text,nullable=False)


class rooms(db.Model):
    room_id=db.Column(db.Integer,nullable=False,primary_key=True)
    room_name=db.Column(db.String(100),nullable=False)


class cpfittings(db.Model):
    fitting_id=db.Column(db.Integer,primary_key=True)
    fitting_name=db.Column(db.String(100), nullable=False)


class product_room_size(db.Model):
    prs_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    p_id=db.Column(db.Integer,db.ForeignKey("products"))
    room_id=db.Column(db.Integer,db.ForeignKey("rooms"))
    s_id=db.Column(db.Integer,db.ForeignKey("sizes"))


class tiles_photos(db.Model):
    photo_id=db.Column(db.Integer,primary_key = True)
    photo_address=db.Column(db.Text,nullable = False,unique = True)
    prs_id=db.Column(db.Integer, db.ForeignKey("product_room_size"))


class product_fitting(db.Model):
    p_fitting_id=db.Column(db.Integer,primary_key=True)
    p_id=db.Column(db.Integer,db.ForeignKey("products"))
    fitting_id=db.Column(db.Integer,db.ForeignKey("cpfittings"))


class cpphotos(db.Model):
    cp_id=db.Column(db.Integer,primary_key = True)
    photo_address=db.Column(db.Text,nullable = False)
    p_fitting_id=db.Column(db.Integer,db.ForeignKey("product_fitting"))


class granites(db.Model):
    granite_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    category=db.Column(db.String(100),nullable = False)


class thick(db.Model):
    thick_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    thick=db.Column(db.String(50),nullable = False)


class granitethick(db.Model):
    gt_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    granite_id=db.Column(db.Integer,db.ForeignKey("granites"))
    thick_id=db.Column(db.Integer,db.ForeignKey("thick"))
    p_id=db.Column(db.Integer,db.ForeignKey("products"))


class granitephoto(db.Model):
    gp_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photo_address=db.Column(db.Text,nullable = False)
    gt_id=db.Column(db.Integer,db.ForeignKey("granitethick"))


class trendingproduct(db.Model):
    tp_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photo_address=db.Column(db.Text,nullable = False)


class basicfinish(db.Model):
    bf_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photo_address=db.Column(db.Text,nullable = False)


class standardfinish(db.Model):
    sf_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photo_address=db.Column(db.Text,nullable = False)


class premiumfinish(db.Model):
    pf_id=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photo_address=db.Column(db.Text,nullable = False)


with app.app_context():
    db.create_all()
    product = products.query.first()
    if not product:
        from sqlalchemy.sql import text
        with open("db/data.sql", 'r', encoding = 'utf-8') as sql_file:
            sql_commands = sql_file.read().split(';')
            for command in sql_commands:
                if command.strip():
                    stmt = text(command)
                    db.session.execute(stmt)

        db.session.commit()